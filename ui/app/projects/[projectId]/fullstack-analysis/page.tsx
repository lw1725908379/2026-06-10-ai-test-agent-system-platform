"use client";
// NOTE  MC8yOmFIVnBZMlhsaUpqbWxvYzZZMGcyY1E9PTo4YjhiOTczZg==

import { MainLayout } from "@/components/layout/main-layout";
import { useLanguage } from "@/providers/LanguageProvider";

function getGitnexusUrl(): string {
  if (typeof window === "undefined") return "";
  const host = window.location.hostname;
  if (host === "localhost" || host === "127.0.0.1") {
    return `http://localhost:5173/gitnexus-web/`;
  }
  return `http://${host}:5173/gitnexus-web/`;
}

export default function FullstackAnalysisPage() {
  const { t } = useLanguage();
  const gitnexusUrl = getGitnexusUrl();

  return (
    <MainLayout title={t("nav.fullstackAnalysis")}>
      <div className="-m-6 h-full">
        <iframe
          src={gitnexusUrl}
          className="h-full w-full border-0"
          title={t("nav.fullstackAnalysis")}
          allow="fullscreen"
        />
      </div>
    </MainLayout>
  );
}
// NOTE  MS8yOmFIVnBZMlhsaUpqbWxvYzZZMGcyY1E9PTo4YjhiOTczZg==
