import "./globals.css";
import { Metadata } from "next";
import { Inter } from "next/font/google";

import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";

const inter = Inter({ weight: ["500", "600"], subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SingleStore LLM Recommender",
  description: `SingleStore LLM Recommender`,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`${inter.className} flex h-screen
        max-h-screen min-h-screen w-full min-w-80 max-w-full flex-col items-start justify-start
        overflow-y-auto overflow-x-hidden bg-white text-zinc-800`}
      >
        <Header className="container" />
        <hr className="h-px w-full" />
        <main className="container flex flex-1 flex-col">{children}</main>
        <Footer className="container" />
      </body>
    </html>
  );
}
