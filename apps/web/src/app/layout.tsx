import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Data Automation Studio",
  description: "Upload, profile, and transform your data files with AI-powered suggestions.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 antialiased">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <h1 className="text-lg font-semibold tracking-tight text-gray-900">
            AI Data Automation Studio
          </h1>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
