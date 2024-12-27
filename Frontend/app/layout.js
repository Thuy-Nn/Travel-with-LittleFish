import {Exo_2, Geist_Mono} from "next/font/google";
import "./globals.css";
import "./icomoon/style.css";

const defaultFont = Exo_2({
  variable: "--font-default",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Travel with Little Fish",
  // description: "Your Travel Companion: Seamless Journeys, Effortless Planning.",
  description: "Travel Smarter, Not Harder. Your All-in-One Travel Assistant.",
};

export default function RootLayout({children}) {
  return (
    <html lang="en">
    <body
      className={`${defaultFont.variable} ${geistMono.variable} antialiased`}
    >
    {children}
    </body>
    </html>
  );
}
