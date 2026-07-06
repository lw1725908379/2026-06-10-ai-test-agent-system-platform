import { apiClient } from "./client";
import type {
  TestCaseInfo,
  TestCaseCreate,
  TestCaseUpdate,
  PaginationInfo,
  Priority,
  TestCaseState,
} from "./types";
// TODO  MC80OmFIVnBZMlhsaUpqbWxvYzZZMUJxTUE9PTpiYmZiYTZkNw==

interface TestCaseResponse {
  success: boolean;
  test_case: TestCaseInfo;
}

interface TestCaseListResponse {
  success: boolean;
  data?: TestCaseInfo[];
  test_cases?: TestCaseInfo[];
  info?: PaginationInfo;
}

interface TestCaseDeleteResponse {
  success: boolean;
  message: string;
}

export interface TestCaseQueryParams {
  p?: number;
  page_size?: number;
  folder_id?: string;
  search?: string;
  priority?: Priority | string;
  status?: TestCaseState | string;
  owner?: string;
  tags?: string;
  minify?: boolean;
}
// FIXME  MS80OmFIVnBZMlhsaUpqbWxvYzZZMUJxTUE9PTpiYmZiYTZkNw==

// 获取项目下的测试用例列表
export function getTestCases(
  projectId: string,
  params?: TestCaseQueryParams
) {
  return apiClient.get<TestCaseListResponse>(
    `/projects/${projectId}/test-cases`,
    { params: params as Record<string, string | number | boolean | undefined> }
  );
}

// 获取文件夹下的测试用例
export function getFolderTestCases(
  projectId: string,
  folderId: string,
  params?: TestCaseQueryParams
) {
  return apiClient.get<TestCaseListResponse>(
    `/projects/${projectId}/folders/${folderId}/test-cases`,
    { params: params as Record<string, string | number | boolean | undefined> }
  );
}

// 获取测试用例详情
export function getTestCase(projectId: string, testCaseId: string) {
  return apiClient.get<TestCaseResponse>(
    `/projects/${projectId}/test-cases/${testCaseId}`
  );
}

// 创建测试用例
export function createTestCase(
  projectId: string,
  folderId: string | null,
  data: TestCaseCreate
) {
  const url = folderId
    ? `/projects/${projectId}/folders/${folderId}/test-cases`
    : `/projects/${projectId}/test-cases`;
  return apiClient.post<TestCaseResponse>(url, data);
}

// 更新测试用例
export function updateTestCase(
  projectId: string,
  testCaseId: string,
  data: TestCaseUpdate
) {
  return apiClient.patch<TestCaseResponse>(
    `/projects/${projectId}/test-cases/${testCaseId}`,
    data
  );
}
// FIXME  Mi80OmFIVnBZMlhsaUpqbWxvYzZZMUJxTUE9PTpiYmZiYTZkNw==

// 删除测试用例
export function deleteTestCase(projectId: string, testCaseId: string) {
  return apiClient.delete<TestCaseDeleteResponse>(
    `/projects/${projectId}/test-cases/${testCaseId}`
  );
}

// 移动测试用例到其他文件夹
export function moveTestCase(
  projectId: string,
  testCaseId: string,
  folderId: string | null
) {
  return apiClient.patch<TestCaseResponse>(
    `/projects/${projectId}/test-cases/${testCaseId}/move`,
    { folder_id: folderId }
  );
}

interface BulkOperationResponse {
  success: boolean;
  message: string;
  affected_count: number;
}

// 批量删除测试用例
export function bulkDeleteTestCases(
  projectId: string,
  testCaseIds: string[]
) {
  return apiClient.delete<BulkOperationResponse>(
    `/projects/${projectId}/test-cases`,
    {
      data: {
        test_case_ids: testCaseIds,
      },
    }
  );
}
// NOTE  My80OmFIVnBZMlhsaUpqbWxvYzZZMUJxTUE9PTpiYmZiYTZkNw==

// 批量更新测试用例
export function bulkUpdateTestCases(
  projectId: string,
  testCaseIds: string[],
  updateData: Partial<TestCaseUpdate>
) {
  return apiClient.post(`/projects/${projectId}/test-cases/bulk/update`, {
    test_case_ids: testCaseIds,
    update_data: updateData,
  });
}

// ==================== 导出相关 ====================

interface ExportBDDResponse {
  success: boolean;
  export_id: string;
  status: string;
  status_url: string;
}

interface ExportStatusResponse {
  success: boolean;
  export_id: string;
  status: string;
  download_url?: string;
  error_message?: string;
}

// 启动 BDD 导出任务
export function exportBDDTestCases(
  projectId: string,
  testCaseIds: string[],
  combineIntoOne: boolean,
  combinedFeature?: string,
  combinedBackground?: string
) {
  return apiClient.post<ExportBDDResponse>(
    `/projects/${projectId}/test-cases/export-bdd`,
    {
      test_case_ids: testCaseIds,
      combine_into_one: combineIntoOne,
      combined_feature: combinedFeature,
      combined_background: combinedBackground,
    }
  );
}

// 查询导出任务状态
export function getExportStatus(exportId: string) {
  return apiClient.get<ExportStatusResponse>(`/exports/${exportId}/status`);
}

// 下载导出文件
export function downloadExport(exportId: string): Promise<Blob> {
  return fetch(`/api/v2/exports/${exportId}/download`).then((res) => {
    if (!res.ok) {
      throw new Error(`下载失败: ${res.status}`);
    }
    return res.blob();
  });
}

// 导出 Excel 测试用例
export function exportExcelTestCases(
  projectId: string,
  testCaseIds: string[]
): Promise<Blob> {
  return fetch(`/api/v2/projects/${projectId}/test-cases/export-excel`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ test_case_ids: testCaseIds }),
  }).then((res) => {
    if (!res.ok) {
      throw new Error(`Excel 导出失败: ${res.status}`);
    }
    return res.blob();
  });
}
