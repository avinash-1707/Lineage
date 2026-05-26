import { Cta } from "@/components/landing/Cta";
import { Features } from "@/components/landing/Features";
import { Footer } from "@/components/landing/Footer";
import { Hero } from "@/components/landing/Hero";
import { Marquee } from "@/components/landing/Marquee";
import { Nav } from "@/components/landing/Nav";
import { Preview } from "@/components/landing/Preview";
import { Process } from "@/components/landing/Process";
import { SideGrid } from "@/components/landing/SideGrid";

export default function Home() {
  return (
    <main className="relative z-10 isolate flex min-h-screen flex-col">
      <Nav />
      <Hero />
      <div className="relative isolate">
        <SideGrid />
        <Marquee />
        <Process />
        <Features />
        <Preview />
        <Cta />
        <Footer />
      </div>
    </main>
  );
}
