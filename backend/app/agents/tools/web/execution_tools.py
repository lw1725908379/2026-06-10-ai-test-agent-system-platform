"""
Web 测试脚本执行工具

提供在 测试目录中执行 Playwright 脚本的功能
"""

import os
import sys
import json
import asyncio
import subprocess
import tempfile
import zipfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

from langchain_core.tools import tool
from sqlalchemy import select

from app.config import settings
from app.config.database import async_session_factory
from app.models.attachment import Attachment, AttachmentEntityType
from app.models.web_function import WebSubFunction
from app.config.minio_client import MinIOClient

# noqa  MC80OmFIVnBZMlhsaUpqbWxvYzZWVGhoZEE9PTpjZWE1ZjA0Yw==

# ============================================================================
# 测试目录配置
# ============================================================================

# 测试服务器根目录
WORKSPACE_TESTS_ROOT = Path(settings.web_mcp_workspace_root) / "tests"


def get_workspace_tests_dir() -> Path:
    """
    获取 WORKSPACE 测试目录路径

    Returns:
        WORKSPACE 测试目录的绝对路径
    """
    return WORKSPACE_TESTS_ROOT


def get_project_root() -> Path:
    """
    获取项目根目录（用于在 测试目录中找到 package.json）

    Returns:
        项目根目录的绝对路径
    """
    # 需要往上找到项目根目录
    return Path(settings.web_mcp_workspace_root)


@tool
async def execute_web_script(
    local_script_path: str,
    framework: str = "playwright",
    reporter: str = "html",
    project_identifier: str = "PR-1",
    sub_function_id: Optional[str] = None
) -> str:
    """
    执行已下载到 MCP 测试目录的 Web 测试脚本

    此工具会：
    1. 验证脚本文件存在于 workspace 测试目录
    2. 执行 Playwright 测试
    3. 生成测试报告（HTML/JSON）
    4. 将测试报告保存到 MinIO
    5. 在数据库中创建测试报告附件记录
    6. 更新子功能的测试运行次数
    7. 清理临时报告文件

    Args:
        local_script_path: 本地脚本文件的完整路径（相对或绝对路径）
        framework: 测试框架 (playwright, jest, pytest)
        reporter: 报告格式 (html, json, list)
        project_identifier: 项目标识符，用于保存测试报告
        sub_function_id: 子功能 ID（可选，用于更新测试统计）

    Returns:
        JSON 格式的执行结果，包含：
        - success: 是否成功
        - script_path: 执行的脚本路径
        - execution_result: 执行结果（stdout, stderr, duration, return_code）
        - report_attachment_id: 测试报告附件 ID（如果生成了报告）
        - error: 错误信息（如果有）

    Example:
        >>> result = await execute_web_script(
        ...     local_script_path="backend/workspace/web/tests/login_test.spec.ts",
        ...     framework="playwright",
        ...     reporter="html",
        ...     project_identifier="PR-3",
        ...     sub_function_id="5ea81a5f-c97b-4a36-a680-13637f1b9eed"
        ... )
    """
    try:
        # 1. 解析脚本路径（兼容 Windows 绝对路径、容器路径、相对路径、纯文件名）
        raw_path = str(local_script_path or "").strip().strip('"').strip("'")
        script_path = Path(raw_path)
        project_root = Path(settings.web_mcp_workspace_root)
        workspace_tests_dir = get_workspace_tests_dir()

        # 归一化：把 Windows 盘符路径映射到容器路径
        # 例：D:/work/.../backend/workspace/web_mcp/tests/xxx.spec.ts
        #     -> /app/backend/workspace/web_mcp/tests/xxx.spec.ts
        if ':' in raw_path.split('/')[0] or raw_path.startswith('\\\\'):
            # Windows 绝对路径，提取 tests 目录之后的部分
            marker = "/web_mcp/"
            if marker in raw_path:
                after_marker = raw_path.split(marker, 1)[1]
                candidate = project_root / after_marker
                if candidate.exists():
                    script_path = candidate
            # 尝试匹配 project_root 内的路径
            if not script_path.exists():
                for candidate in project_root.rglob(script_path.name):
                    if candidate.exists():
                        script_path = candidate
                        break

        if not script_path.exists():
            # 尝试在 workspace 测试目录中按文件名查找
            if script_path.name:
                for candidate in workspace_tests_dir.glob(f"*{script_path.stem}*"):
                    if candidate.exists():
                        script_path = candidate
                        break

        # 2. 验证脚本文件存在
        if not script_path.exists():
            return json.dumps({
                "success": False,
                "error": f"脚本文件不存在: {script_path}（已尝试解析路径: {raw_path}）"
            }, ensure_ascii=False, indent=2)

        script_filename = script_path.name

        print(f"[Web Script Execution] 准备执行脚本: {script_path}")

        # 3. 确定相对路径（相对于项目根目录）
        try:
            relative_path = script_path.relative_to(project_root)
        except ValueError:
            # 路径不在 project_root 下，用文件名作为相对路径
            relative_path = Path("tests") / script_filename

        print(f"[Web Script Execution] 项目根目录: {project_root}")
        print(f"[Web Script Execution] 相对脚本路径: {relative_path}")

        # 5. 执行脚本
        execution_result = await _execute_script_internal(
            script_path=str(relative_path),
            script_filename=script_filename,
            framework=framework,
            reporter=reporter,
            project_root=str(project_root)
        )

        # 6. 保存测试报告到 MinIO（如果生成了 HTML 报告）
        report_attachment_id = None
        if sub_function_id and reporter == "html" and execution_result.get("report_path"):
            # 获取子功能信息
            async with async_session_factory() as db:
                sub_function_result = await db.execute(
                    select(WebSubFunction).where(WebSubFunction.id == UUID(sub_function_id))
                )
                sub_function = sub_function_result.scalar_one_or_none()

            if sub_function:
                report_attachment_id = await _save_test_report(
                    sub_function_id=sub_function_id,
                    project_identifier=project_identifier,
                    sub_function=sub_function,
                    report_path=execution_result["report_path"],
                    execution_result=execution_result,
                    project_root=str(project_root)
                )

                # 6. 保存测试视频（如果生成了）
                video_attachment_id = None
                if execution_result.get("video_path"):
                    video_attachment_id = await _save_test_video(
                        video_path=execution_result["video_path"],
                        sub_function_id=sub_function_id,
                        project_identifier=project_identifier,
                        sub_function=sub_function,
                        project_root=str(project_root)
                    )
                    if video_attachment_id:
                        print(f"[Web Script Execution] 测试视频已保存，附件ID: {video_attachment_id}")

                # 6.1 保存控制台日志（如果生成了）
                log_attachment_id = None
                if execution_result.get("console_log_path"):
                    log_attachment_id = await _save_console_log(
                        log_path=execution_result["console_log_path"],
                        sub_function_id=sub_function_id,
                        project_identifier=project_identifier,
                        sub_function=sub_function,
                        execution_result=execution_result
                    )
                    if log_attachment_id:
                        print(f"[Web Script Execution] 控制台日志已保存，附件ID: {log_attachment_id}")

                # 7. 更新子功能的测试运行次数
                try:
                    async with async_session_factory() as db:
                        sub_function_result = await db.execute(
                            select(WebSubFunction).where(WebSubFunction.id == UUID(sub_function_id))
                        )
                        sub_function = sub_function_result.scalar_one_or_or_none()

                        if sub_function:
                            # 递增测试运行次数
                            sub_function.total_test_runs = (sub_function.total_test_runs or 0) + 1

                            # 更新最后运行状态
                            if execution_result.get("success"):
                                sub_function.last_run_status = "passed"
                            else:
                                sub_function.last_run_status = "failed"

                            await db.commit()
                            print(f"[Web Script Execution] 已更新子功能 {sub_function_id} 的测试运行次数")
                except Exception as e:
                    print(f"[Web Script Execution] 更新子功能测试运行次数失败: {e}")

        # 8. 返回结果
        result = {
            "success": True,
            "script_path": str(script_path),
            "script_filename": script_filename,
            "execution_result": execution_result
        }

        if report_attachment_id:
            result["report_attachment_id"] = report_attachment_id
            result["message"] = "脚本执行完成，测试报告已保存"

        if sub_function_id:
            result["sub_function_id"] = sub_function_id
# pragma: no cover  MS80OmFIVnBZMlhsaUpqbWxvYzZWVGhoZEE9PTpjZWE1ZjA0Yw==

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return json.dumps({
            "success": False,
            "error": f"执行脚本时发生错误: {str(e)}"
        }, ensure_ascii=False, indent=2)


async def _execute_script_internal(
    script_path: str,
    script_filename: str,
    framework: str,
    reporter: str,
    project_root: str
) -> Dict[str, Any]:
    """
    内部执行脚本函数

    Args:
        script_path: 脚本文件相对路径（相对于 project_root）
        script_filename: 脚本文件名
        framework: 测试框架
        reporter: 报告格式
        project_root: 项目根目录

    Returns:
        执行结果字典
    """
    try:
        start_time = datetime.now()

        # 确定测试命令
        is_windows = sys.platform == "win32"

        if framework == "playwright":
            # 优先使用本地的 playwright（避免每次重新安装依赖）
            local_playwright_bin = str(Path(project_root) / "node_modules" / ".bin" / "playwright")
            if Path(local_playwright_bin).exists():
                # 使用本地安装的 playwright
                playwright_cmd = local_playwright_bin
                print(f"[Web Script Execution] 使用本地 playwright: {playwright_cmd}")
            elif is_windows:
                playwright_cmd = "npx playwright"
            else:
                playwright_cmd = "npx playwright"

            if reporter == "html":
                # HTML 报告需要指定输出目录
                if is_windows:
                    cmd = f'{playwright_cmd} test {script_filename} --reporter=html'
                else:
                    cmd = [playwright_cmd, "test", script_filename, "--reporter=html"]
            else:
                if is_windows:
                    cmd = f'{playwright_cmd} test {script_filename} --reporter={reporter}'
                else:
                    cmd = [playwright_cmd, "test", script_filename, f"--reporter={reporter}"]
        else:
            return {
                "success": False,
                "error": f"不支持的测试框架: {framework}，Web 测试仅支持 playwright"
            }

        print(f"[Web Script Execution] 执行命令: {cmd if is_windows else ' '.join(cmd)}")
        print(f"[Web Script Execution] 工作目录: {project_root}")

        # 准备环境变量（设置 CI=1 禁用 Playwright HTML reporter 自动打开浏览器）
        env = os.environ.copy()
        if reporter == "html":
            env['CI'] = '1'

        # 执行测试（使用异步子进程，避免阻塞 event loop）
        if is_windows:
            # Windows 下通过 shell 执行
            result = subprocess.run(
                cmd,
                cwd=project_root,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=300,  # 5分钟超时
                shell=is_windows,
                env=env
            )
        else:
            # Linux/容器内使用异步子进程，不阻塞 asyncio event loop
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=project_root,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                start_new_session=True,  # 新进程组，便于超时后清理整个进程树
            )
            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    proc.communicate(), timeout=300  # 5分钟超时
                )
                stdout = stdout_bytes.decode('utf-8', errors='replace')
                stderr = stderr_bytes.decode('utf-8', errors='replace')
                return_code = proc.returncode
            except asyncio.TimeoutError:
                # 杀掉整个进程组（含 playwright 子进程 chromium/ffmpeg），避免子进程挂起
                try:
                    import signal
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except Exception:
                    # 进程组获取失败时退化为杀主进程
                    proc.kill()
                try:
                    await asyncio.wait_for(proc.wait(), timeout=10)
                except Exception:
                    pass
                return {
                    "success": False,
                    "error": "脚本执行超时（超过5分钟）",
                    "timed_out": True,
                }

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
# noqa  Mi80OmFIVnBZMlhsaUpqbWxvYzZWVGhoZEE9PTpjZWE1ZjA0Yw==

        # 解析输出（异步分支已设置 stdout/stderr/return_code，Windows 分支从 result 读取）
        if is_windows:
            stdout = result.stdout
            stderr = result.stderr
            return_code = result.returncode

        print(f"[Web Script Execution] 执行完成，返回码: {return_code}")
        print(f"[Web Script Execution] 执行时间: {duration:.2f}s")

        # 检查是否生成了 HTML 报告
        report_path = None
        video_path = None
        if reporter == "html":
            report_dir = Path(project_root) / "playwright-report"
            index_html = report_dir / "index.html"
            if index_html.exists():
                report_path = str(report_dir)
                print(f"[Web Script Execution] HTML 报告已生成: {report_path}")

            # 查找生成的视频文件
            video_dir = Path(project_root) / "test-results"
            if video_dir.exists():
                video_files = list(video_dir.glob("*.webm")) + list(video_dir.glob("*.mp4"))
                if video_files:
                    # 获取最新的视频文件
                    latest_video = max(video_files, key=lambda p: p.stat().st_mtime)
                    video_path = str(latest_video)
                    print(f"[Web Script Execution] 视频已生成: {video_path}")

        # 保存控制台日志到文件
        console_log_path = None
        log_dir = Path(project_root) / "test-results"
        if stdout or stderr:
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_filename = f"console_{timestamp}.log"
                log_path = log_dir / log_filename

                log_content = f"=== Playwright Test Execution Log ===\n"
                log_content += f"Start Time: {start_time.isoformat()}\n"
                log_content += f"End Time: {end_time.isoformat()}\n"
                log_content += f"Duration: {duration:.2f}s\n"
                log_content += f"Return Code: {return_code}\n"
                log_content += f"\n=== STDOUT ===\n{stdout}\n"
                log_content += f"\n=== STDERR ===\n{stderr}\n"

                log_path.write_text(log_content, encoding='utf-8')
                console_log_path = str(log_path)
                print(f"[Web Script Execution] 控制台日志已保存: {console_log_path}")
            except Exception as e:
                print(f"[Web Script Execution] 保存控制台日志失败: {e}")

        return {
            "success": return_code == 0,
            "return_code": return_code,
            "duration": duration,
            "stdout": stdout,
            "stderr": stderr,
            "report_path": report_path,
            "video_path": video_path,
            "console_log_path": console_log_path,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "脚本执行超时（超过5分钟）"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"执行脚本时发生错误: {str(e)}"
        }


async def _save_test_report(
    sub_function_id: str,
    project_identifier: str,
    sub_function: WebSubFunction,
    report_path: str,
    execution_result: Dict[str, Any],
    project_root: str
) -> Optional[str]:
    """
    保存测试报告到 MinIO 并创建附件记录

    Args:
        sub_function_id: 子功能 ID
        project_identifier: 项目标识符
        sub_function: 子功能对象
        report_path: 报告目录路径
        execution_result: 执行结果
        project_root: 项目根目录

    Returns:
        附件 ID，如果保存失败则返回 None
    """
    try:
        # 1. 将报告目录打包成 ZIP
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"web_test_report_{timestamp}.zip"
        zip_path = Path(project_root) / zip_filename

        print(f"[Web Report] 打包测试报告: {report_path} -> {zip_path}")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            report_dir = Path(report_path)
            for file_path in report_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(report_dir)
                    zipf.write(file_path, arcname)

        # 2. 读取 ZIP 文件内容
        with open(zip_path, 'rb') as f:
            zip_bytes = f.read()

        # 3. 上传到 MinIO
        object_name = f"web-tests/{project_identifier}/sub-functions/{sub_function_id}/test-report-{timestamp}.zip"
        MinIOClient.upload_bytes(
            object_name=object_name,
            data=zip_bytes,
            content_type="application/zip"
        )

        print(f"[Web Report] 报告已上传到 MinIO: {object_name}")

        # 4. 创建附件记录
        async with async_session_factory() as session:
            # 生成报告描述
            duration = execution_result.get("duration", 0)
            stdout = execution_result.get("stdout", "")

            # 尝试解析测试结果
            passed_count = stdout.count("✓") + stdout.count("passed")
            failed_count = stdout.count("✘") + stdout.count("failed")

            description = f"Web 测试报告 - {sub_function.display_name}\n"
            description += f"执行时间: {duration:.2f}秒\n"
            if passed_count > 0 or failed_count > 0:
                description += f"通过: {passed_count} | 失败: {failed_count}"

            # 创建附件
            attachment = Attachment(
                entity_type=AttachmentEntityType.WEB_TEST_REPORT,
                entity_id=UUID(sub_function_id),
                project_id=sub_function.project_id,
                file_name=f"web-test-report-{timestamp}.zip",
                file_size=len(zip_bytes),
                content_type="application/zip",
                object_name=object_name,
                description=description,
                created_by="web-agent"
            )

            session.add(attachment)
            await session.commit()
            await session.refresh(attachment)
# fmt: off  My80OmFIVnBZMlhsaUpqbWxvYzZWVGhoZEE9PTpjZWE1ZjA0Yw==

            print(f"[Web Report] 附件记录已创建: {attachment.id}")

            # 5. 清理临时 ZIP 文件
            try:
                zip_path.unlink()
                print(f"[Web Report] 临时 ZIP 文件已清理: {zip_path}")
            except Exception as e:
                print(f"[Web Report] 清理临时 ZIP 文件失败: {e}")

            # 6. 清理报告目录
            try:
                shutil.rmtree(report_path)
                print(f"[Web Report] 报告目录已清理: {report_path}")
            except Exception as e:
                print(f"[Web Report] 清理报告目录失败: {e}")

            return str(attachment.id)

    except Exception as e:
        print(f"[Web Report] 保存测试报告失败: {e}")
        import traceback
        traceback.print_exc()
        return None


async def _save_test_video(
    video_path: str,
    sub_function_id: str,
    project_identifier: str,
    sub_function: WebSubFunction,
    project_root: str
) -> Optional[str]:
    """
    保存测试视频到 MinIO 并创建附件记录

    Args:
        video_path: 视频文件路径
        sub_function_id: 子功能 ID
        project_identifier: 项目标识符
        sub_function: 子功能对象
        project_root: 项目根目录

    Returns:
        附件 ID，如果保存失败则返回 None
    """
    if not video_path or not Path(video_path).exists():
        print(f"[Web Video] 视频文件不存在: {video_path}")
        return None

    try:
        video_file_path = Path(video_path)

        # 1. 读取视频文件内容
        with open(video_file_path, 'rb') as f:
            video_bytes = f.read()

        # 2. 上传到 MinIO
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_name = f"web-tests/{project_identifier}/sub-functions/{sub_function_id}/test-video-{timestamp}.webm"
        MinIOClient.upload_bytes(
            object_name=object_name,
            data=video_bytes,
            content_type="video/webm"
        )

        print(f"[Web Video] 视频已上传到 MinIO: {object_name}")

        # 3. 创建附件记录
        async with async_session_factory() as session:
            duration = 0
            description = f"Web 测试执行录像 - {sub_function.display_name}"

            # 创建附件
            attachment = Attachment(
                entity_type=AttachmentEntityType.WEB_TEST_REPORT,
                entity_id=UUID(sub_function_id),
                project_id=sub_function.project_id,
                file_name=f"test-video-{timestamp}.webm",
                file_size=len(video_bytes),
                content_type="video/webm",
                object_name=object_name,
                description=description,
                created_by="web-agent"
            )

            session.add(attachment)
            await session.commit()
            await session.refresh(attachment)

            print(f"[Web Video] 视频附件记录已创建: {attachment.id}")

            # 4. 清理临时视频文件
            try:
                video_file_path.unlink()
                print(f"[Web Video] 临时视频文件已清理: {video_file_path}")
            except Exception as e:
                print(f"[Web Video] 清理临时视频文件失败: {e}")

            return str(attachment.id)

    except Exception as e:
        print(f"[Web Video] 保存测试视频失败: {e}")
        import traceback
        traceback.print_exc()
        return None


async def _save_console_log(
    log_path: str,
    sub_function_id: str,
    project_identifier: str,
    sub_function: WebSubFunction,
    execution_result: Dict[str, Any]
) -> Optional[str]:
    """
    保存测试控制台日志到 MinIO 并创建附件记录

    Args:
        log_path: 日志文件路径
        sub_function_id: 子功能 ID
        project_identifier: 项目标识符
        sub_function: 子功能对象
        execution_result: 执行结果

    Returns:
        附件 ID，如果保存失败则返回 None
    """
    if not log_path or not Path(log_path).exists():
        print(f"[Web Log] 日志文件不存在: {log_path}")
        return None

    try:
        log_file_path = Path(log_path)

        # 1. 读取日志文件内容
        with open(log_file_path, 'rb') as f:
            log_bytes = f.read()

        # 2. 上传到 MinIO
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_name = f"web-tests/{project_identifier}/sub-functions/{sub_function_id}/test-log-{timestamp}.log"
        MinIOClient.upload_bytes(
            object_name=object_name,
            data=log_bytes,
            content_type="text/plain"
        )

        print(f"[Web Log] 日志已上传到 MinIO: {object_name}")

        # 3. 创建附件记录
        async with async_session_factory() as session:
            duration = execution_result.get("duration", 0)
            description = f"Web 测试执行日志 - {sub_function.display_name}\n"
            description += f"执行时间: {duration:.2f}秒"

            # 创建附件
            attachment = Attachment(
                entity_type=AttachmentEntityType.WEB_TEST_REPORT,
                entity_id=UUID(sub_function_id),
                project_id=sub_function.project_id,
                file_name=f"test-log-{timestamp}.log",
                file_size=len(log_bytes),
                content_type="text/plain",
                object_name=object_name,
                description=description,
                created_by="web-agent"
            )

            session.add(attachment)
            await session.commit()
            await session.refresh(attachment)

            print(f"[Web Log] 日志附件记录已创建: {attachment.id}")

            # 4. 清理临时日志文件
            try:
                log_file_path.unlink()
                print(f"[Web Log] 临时日志文件已清理: {log_file_path}")
            except Exception as e:
                print(f"[Web Log] 清理临时日志文件失败: {e}")

            return str(attachment.id)

    except Exception as e:
        print(f"[Web Log] 保存控制台日志失败: {e}")
        import traceback
        traceback.print_exc()
        return None


@tool
async def get_test_execution_status(
    execution_id: str
) -> str:
    """
    获取测试执行状态（占位符，未来可扩展为异步执行查询）

    Args:
        execution_id: 执行 ID

    Returns:
        JSON 格式的执行状态
    """
    return json.dumps({
        "success": True,
        "execution_id": execution_id,
        "status": "completed",
        "message": "当前版本仅支持同步执行，不支持异步状态查询"
    }, ensure_ascii=False, indent=2)
