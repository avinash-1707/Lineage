import { Cta } from "@/components/landing/Cta";
import { Features } from "@/components/landing/Features";
import { Footer } from "@/components/landing/Footer";
import { Hero } from "@/components/landing/Hero";
import { Marquee } from "@/components/landing/Marquee";
import { Nav } from "@/components/landing/Nav";
import { Preview } from "@/components/landing/Preview";
import { Process } from "@/components/landing/Process";

export default function Home() {
  return (
    <main className="relative isolate flex min-h-screen flex-col">
      <Nav />
      <Hero />
      <Marquee />
      <Process />
      <Features />
      <Preview />
      <Cta />
      <Footer />
    </main>
  );
}
