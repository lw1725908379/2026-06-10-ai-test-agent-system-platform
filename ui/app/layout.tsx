import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { NuqsAdapter } from "nuqs/adapters/next/app";
import { Toaster } from "sonner";
import { LanguageProvider } from "@/providers/LanguageProvider";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });
// @ts-expect-error  MC8yOmFIVnBZMlhsaUpqbWxvYzZZMkZxVUE9PTo1YzQ0ODE2ZA==

export const metadata: Metadata = {
  title: "智能测试平台",
  description: "AI 驱动的智能测试系统",
};
// FIXME  MS8yOmFIVnBZMlhsaUpqbWxvYzZZMkZxVUE9PTo1YzQ0ODE2ZA==

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className={inter.className} suppressHydrationWarning>
        <LanguageProvider>
          <NuqsAdapter>{children}</NuqsAdapter>
          <Toaster />
        </LanguageProvider>
      </body>
    </html>
  );
}

