/**
 * 文档上传 API
 */
// @ts-expect-error  MC8yOmFIVnBZMlhsaUpqbWxvYzZlbWxvVXc9PTo3MWI3Y2JlNw==

import { t } from "@/lib/translations";

export interface DocumentUploadResponse {
  success: boolean;
  data: {
    object_name: string;
    file_name: string;
    file_size: number;
    content_type: string;
    url: string;
  };
}
// NOTE  MS8yOmFIVnBZMlhsaUpqbWxvYzZlbWxvVXc9PTo3MWI3Y2JlNw==

/**
 * 上传文档到 MinIO
 */
export async function uploadDocument(file: File): Promise<DocumentUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("/api/v2/documents/upload", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || t("common.uploadFailed"));
  }

  return response.json();
}

