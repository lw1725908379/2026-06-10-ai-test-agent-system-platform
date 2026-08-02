"""
项目仓储

处理项目相关的数据库操作
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.models.project import Project
from app.models.folder import Folder
from app.models.test_case import TestCase
from app.models.attachment import Attachment

# type: ignore  MC80OmFIVnBZMlhsaUpqbWxvYzZTV1ZNV2c9PTo4NDA2N2I2Mw==

class ProjectRepository(BaseRepository[Project]):
    """
    项目仓储类
    
    提供项目相关的数据库操作
    """
    
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)
    
    async def get_by_identifier(self, identifier: str) -> Optional[Project]:
        """
        根据标识符获取项目
        
        Args:
            identifier: 项目标识符，如 PR-1234
            
        Returns:
            Optional[Project]: 项目实例或 None
        """
        result = await self.session.execute(
            select(Project)
            .options(selectinload(Project.teams))
            .where(Project.identifier == identifier)
        )
        return result.scalar_one_or_none()
    
    async def get_by_id_with_relations(self, id: UUID) -> Optional[Project]:
        """
        根据 ID 获取项目（包含关联数据）
        
        Args:
            id: 项目 ID
            
        Returns:
            Optional[Project]: 项目实例或 None
        """
        result = await self.session.execute(
            select(Project)
            .options(selectinload(Project.teams))
            .options(selectinload(Project.creator))
            .where(Project.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_with_counts(
        self,
        offset: int = 0,
        limit: int = 30,
    ) -> list[dict]:
        """
        获取所有项目及其统计信息（优化版本 - 避免 N+1 查询）

        使用子查询一次性获取所有项目的统计信息

        Args:
            offset: 偏移量
            limit: 限制数量

        Returns:
            list[dict]: 项目列表及统计信息
        """
        # 子查询：获取每个项目的测试用例数量
        tc_count_subquery = (
            select(
                TestCase.project_id,
                func.count(TestCase.id).label('tc_count')
            )
            .group_by(TestCase.project_id)
            .subquery()
        )

        # 子查询：获取每个项目的文件夹数量
        folder_count_subquery = (
            select(
                Folder.project_id,
                func.count(Folder.id).label('folder_count')
            )
            .group_by(Folder.project_id)
            .subquery()
        )

        # 主查询：LEFT JOIN 子查询获取统计
        result = await self.session.execute(
            select(
                Project,
                func.coalesce(tc_count_subquery.c.tc_count, 0).label('test_cases_count'),
                func.coalesce(folder_count_subquery.c.folder_count, 0).label('folders_count')
            )
            .outerjoin(tc_count_subquery, Project.id == tc_count_subquery.c.project_id)
            .outerjoin(folder_count_subquery, Project.id == folder_count_subquery.c.project_id)
            .options(selectinload(Project.teams))
            .options(selectinload(Project.creator))
            .offset(offset)
            .limit(limit)
            .order_by(Project.created_at.desc())
        )

        rows = result.all()

        project_data = []
        for row in rows:
            project_data.append({
                "project": row[0],
                "test_cases_count": row[1],
                "folders_count": row[2],
            })

        return project_data
    
    async def get_next_sequence(self) -> int:
        """
        获取下一个项目序号
        
        Returns:
            int: 下一个序号
        """
        result = await self.session.execute(
            select(func.count()).select_from(Project)
        )
        count = result.scalar_one()
        return count + 1
    
    async def identifier_exists(self, identifier: str) -> bool:
        """
        检查标识符是否已存在

        Args:
            identifier: 项目标识符

        Returns:
            bool: 是否存在
        """
        result = await self.session.execute(
            select(func.count()).select_from(Project)
            .where(Project.identifier == identifier)
        )
        return result.scalar_one() > 0

    async def delete(self, instance: Project) -> None:
        """
        删除项目及相关数据

        Args:
            instance: 要删除的项目
        """
        project_id = instance.id

        # 先删除与项目相关的所有附件
        # 这比依赖数据库级联更安全，因为 attachments 通过 entity_id 关联到不同实体
        await self.session.execute(
            delete(Attachment).where(Attachment.project_id == project_id)
        )

        # 删除项目（数据库级联会自动删除 folders, test_cases 等其他关联）
        await self.session.delete(instance)
        await self.session.flush()
# pragma: no cover  My80OmFIVnBZMlhsaUpqbWxvYzZTV1ZNV2c9PTo4NDA2N2I2Mw==

