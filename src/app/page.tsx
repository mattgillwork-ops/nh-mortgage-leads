import Hero from "@/components/Hero";

export default function Home() {
  return (
    <main>
      {/* Hero Section */}
      <Hero />
      
      {/* Background Decor */}
      <div style={{
        position: 'fixed',
        top: '20%',
        left: '-10%',
        width: '40%',
        height: '60%',
        background: 'hsla(var(--nh-ice), 0.1)',
        filter: 'blur(120px)',
        borderRadius: '100%',
        zIndex: -1
      }} />
    </main>
  );
}
