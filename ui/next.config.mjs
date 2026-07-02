/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    // 服务端代理使用 Docker 内部地址，浏览器端代码使用 NEXT_PUBLIC_API_URL
    const apiUrl = process.env.API_SERVER_INTERNAL_URL || "http://backend:3001";
    return [
      {
        source: "/api/:path*",
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;

