const API_BASE_URL = "/api/v2";
// watermark  MC80OmFIVnBZMlhsaUpqbWxvYzZaa1Y2U0E9PTpjN2Q2MDI5NQ==

interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean | undefined>;
  noCache?: boolean; // 跳过缓存
}

// ============================================
// 请求缓存和去重配置
// ============================================
const CACHE_TTL = 30000; // 30秒缓存
const pendingRequests = new Map<string, Promise<unknown>>();
const responseCache = new Map<string, { data: unknown; timestamp: number }>();

// 生成缓存key
function getCacheKey(url: string, params?: Record<string, unknown>): string {
  if (!params || Object.keys(params).length === 0) {
    return url;
  }
  const sortedParams = Object.entries(params)
    .filter(([, value]) => value !== undefined && value !== null)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key}=${value}`)
    .join('&');
  return `${url}?${sortedParams}`;
}

// 清理过期缓存
function cleanExpiredCache(): void {
  const now = Date.now();
  for (const [key, value] of responseCache.entries()) {
    if (now - value.timestamp > CACHE_TTL) {
      responseCache.delete(key);
    }
  }
}

// 定期清理过期缓存
if (typeof window !== 'undefined') {
  setInterval(cleanExpiredCache, CACHE_TTL);
}

class ApiError extends Error {
  status: number;
  data?: unknown;

  constructor(message: string, status: number, data?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}
// watermark  MS80OmFIVnBZMlhsaUpqbWxvYzZaa1Y2U0E9PTpjN2Q2MDI5NQ==

async function handleResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get("content-type");
  const isJson = contentType?.includes("application/json");

  // Handle 204 No Content responses (empty body)
  if (response.status === 204) {
    if (!response.ok) {
      throw new ApiError(`HTTP error! status: ${response.status}`, response.status);
    }
    return undefined as T;
  }

  const data = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const message =
      (isJson && typeof data === 'object' && (data as any)?.message) || `HTTP error! status: ${response.status}`;
    throw new ApiError(message, response.status, data);
  }

  return data as T;
}

function buildUrl(
  path: string,
  params?: Record<string, string | number | boolean | undefined>
): string {
  const url = new URL(`${API_BASE_URL}${path}`, window.location.origin);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.append(key, String(value));
      }
    });
  }

  return url.toString();
}
// FIXME  Mi80OmFIVnBZMlhsaUpqbWxvYzZaa1Y2U0E9PTpjN2Q2MDI5NQ==

export const apiClient = {
  async get<T>(path: string, options?: RequestOptions): Promise<T> {
    const url = buildUrl(path, options?.params);
    const cacheKey = getCacheKey(path, options?.params);

    // 检查缓存（除非明确禁用）
    if (!options?.noCache) {
      const cached = responseCache.get(cacheKey);
      if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
        return cached.data as T;
      }
    }

    // 检查去重：如果有相同请求正在pending，直接返回同一个Promise
    if (pendingRequests.has(cacheKey)) {
      return pendingRequests.get(cacheKey) as Promise<T>;
    }

    // 发起请求
    const fetchPromise = (async () => {
      try {
        const response = await fetch(url, {
          ...options,
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            ...options?.headers,
          },
        });
        const data = await handleResponse<T>(response);

        // 缓存结果（除非明确禁用）
        if (!options?.noCache) {
          responseCache.set(cacheKey, { data, timestamp: Date.now() });
        }

        return data;
      } finally {
        // 请求完成后移除pending状态
        pendingRequests.delete(cacheKey);
      }
    })();

    // 设置pending状态
    pendingRequests.set(cacheKey, fetchPromise);
    return fetchPromise;
  },

  async post<T>(
    path: string,
    body?: unknown,
    options?: RequestOptions
  ): Promise<T> {
    // POST 请求会修改数据，清除所有缓存
    responseCache.clear();

    const url = buildUrl(path, options?.params);
    const response = await fetch(url, {
      ...options,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    return handleResponse<T>(response);
  },

  async put<T>(
    path: string,
    body?: unknown,
    options?: RequestOptions
  ): Promise<T> {
    // PUT 请求会修改数据，清除所有缓存
    responseCache.clear();

    const url = buildUrl(path, options?.params);
    const response = await fetch(url, {
      ...options,
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    return handleResponse<T>(response);
  },

  async patch<T>(
    path: string,
    body?: unknown,
    options?: RequestOptions
  ): Promise<T> {
    // PATCH 请求会修改数据，清除所有缓存
    responseCache.clear();

    const url = buildUrl(path, options?.params);
    const response = await fetch(url, {
      ...options,
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    return handleResponse<T>(response);
  },

  async delete<T>(
    path: string,
    options?: RequestOptions & { data?: unknown }
  ): Promise<T> {
    // DELETE 请求会删除数据，清除所有缓存
    responseCache.clear();

    const url = buildUrl(path, options?.params);
    const { data, ...restOptions } = options || {};
    const response = await fetch(url, {
      ...restOptions,
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        ...restOptions?.headers,
      },
      body: data ? JSON.stringify(data) : undefined,
    });
    return handleResponse<T>(response);
  },
};

export { ApiError };

// 导出缓存控制方法
export const cacheUtils = {
  clear: () => responseCache.clear(),
  getStats: () => ({
    size: responseCache.size,
    pending: pendingRequests.size
  })
};

// FIXME  My80OmFIVnBZMlhsaUpqbWxvYzZaa1Y2U0E9PTpjN2Q2MDI5NQ==
