import type { Metadata } from "next";
import { ThemeProvider } from "next-themes";
import { NuqsAdapter } from "nuqs/adapters/next/app";
import { Toaster } from "sonner";
import { LanguageProvider } from "@/providers/LanguageProvider";
import "./globals.css";
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
      <body className="font-sans" suppressHydrationWarning>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <LanguageProvider>
            <NuqsAdapter>{children}</NuqsAdapter>
            <Toaster />
          </LanguageProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}

