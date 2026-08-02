/** @type {import('next').NextConfig} */
const nextConfig = {
  // 忽略 TypeScript 类型错误（项目使用 @ts-expect-error 水印抑制历史类型警告）
  typescript: {
    ignoreBuildErrors: true,
  },
  async rewrites() {
    const apiUrl = process.env.API_SERVER_INTERNAL_URL || "http://backend:3001";
    const langgraphUrl = process.env.LANGGRAPH_SERVER_URL || "http://langgraph-server:2026";
    return [
      {
        source: "/api/langgraph/:path*",
        destination: `${langgraphUrl}/:path*`,
      },
      {
        source: "/api/:path*",
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;

