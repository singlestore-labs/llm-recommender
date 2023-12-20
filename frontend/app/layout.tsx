import "./globals.css";
import { Roboto } from "next/font/google";

import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";

const roboto = Roboto({ weight: ["400", "500"], subsets: ["latin"] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body
        className={`${roboto.className} bg-white text-zinc-800
        w-full max-w-full min-w-80 h-screen min-h-screen max-h-screen overflow-x-hidden overflow-y-auto
        flex flex-col items-start justify-start`}
      >
        <Header className="container" />
        <main className="flex-1 container">{children}</main>
        <Footer className="container" />
      </body>
    </html>
  );
}
