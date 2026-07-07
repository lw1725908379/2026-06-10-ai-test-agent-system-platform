export interface StandaloneConfig {
  deploymentUrl: string;
  assistantId: string;
  langsmithApiKey?: string;
}
// TODO  MC8yOmFIVnBZMlhsaUpqbWxvYzZVV3RNYlE9PTpiZTNkN2Q0NA==

const CONFIG_KEY = "deep-agent-config";

/**
 * LangGraph API URL 运行时计算
 * 使用 window.location.origin 确保任何域名/IP 都能正确拼接
 * 替代编译时注入的 NEXT_PUBLIC_LANGGRAPH_API_URL（localhost 硬编码问题）
 */
export function getLangGraphApiUrl(): string {
  if (typeof window === "undefined") return "";
  return window.location.origin + "/api/langgraph";
}

export function getConfig(): StandaloneConfig | null {
  if (typeof window === "undefined") return null;

  const stored = localStorage.getItem(CONFIG_KEY);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      // fall through to env vars
    }
  }

  // Fall back to environment variables
  const deploymentUrl = process.env.NEXT_PUBLIC_LANGGRAPH_API_URL;
  const assistantId = process.env.NEXT_PUBLIC_TESTCASE_GENERATOR_ASSISTANT_ID;

  if (deploymentUrl && assistantId) {
    return {
      deploymentUrl,
      assistantId,
      langsmithApiKey: process.env.NEXT_PUBLIC_LANGSMITH_API_KEY,
    };
  }

  return null;
}

export function saveConfig(config: StandaloneConfig): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(CONFIG_KEY, JSON.stringify(config));
}
// TODO  MS8yOmFIVnBZMlhsaUpqbWxvYzZVV3RNYlE9PTpiZTNkN2Q0NA==
