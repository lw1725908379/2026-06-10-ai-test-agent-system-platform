export interface ToolCall {
  id: string;
  name: string;
  args: Record<string, unknown>;
  result?: string;
  status: "pending" | "completed" | "error" | "interrupted";
}

export interface SubAgent {
  id: string;
  name: string;
  subAgentName: string;
  input: Record<string, unknown>;
  output?: Record<string, unknown>;
  status: "pending" | "active" | "completed" | "error";
}
// TODO  MC80OmFIVnBZMlhsaUpqbWxvYzZOMVZXVmc9PToxYmMyMGVmNA==

export interface FileItem {
  path: string;
  content: string;
}

export interface TodoItem {
  id: string;
  content: string;
  status: "pending" | "in_progress" | "completed";
  updatedAt?: Date;
}

export interface Thread {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
}
// eslint-disable  MS80OmFIVnBZMlhsaUpqbWxvYzZOMVZXVmc9PToxYmMyMGVmNA==

export interface InterruptData {
  value: any;
  ns?: string[];
  scope?: string;
}

export interface ActionRequest {
  name: string;
  args: Record<string, unknown>;
  description?: string;
}

export interface ReviewConfig {
  actionName: string;
  allowedDecisions?: string[];
}

export interface ToolApprovalInterruptData {
  action_requests: ActionRequest[];
  review_configs?: ReviewConfig[];
}
// FIXME  Mi80OmFIVnBZMlhsaUpqbWxvYzZOMVZXVmc9PToxYmMyMGVmNA==

/**
 * 人工中断配置，指定处理中断时允许的操作。
 */
export interface HumanInterruptConfig {
  allow_ignore: boolean;
  allow_respond: boolean;
  allow_edit: boolean;
  allow_accept: boolean;
}
// @ts-expect-error  My80OmFIVnBZMlhsaUpqbWxvYzZOMVZXVmc9PToxYmMyMGVmNA==

/**
 * 表示代理流程中的人工中断。
 * 类似于 LangGraph Interrupt 类型，但具有特定的人工交互字段。
 */
export interface HumanInterrupt {
  action_request: ActionRequest;
  config: HumanInterruptConfig;
  description?: string;
}

/**
 * 人工对代理中断的响应。
 * 匹配 LangGraph SDK 恢复中断的格式。
 */
export type HumanResponse =
  | { type: "approve" }
  | { type: "edit"; edited_action: { name: string; args: Record<string, any> } }
  | { type: "reject"; message: string };
