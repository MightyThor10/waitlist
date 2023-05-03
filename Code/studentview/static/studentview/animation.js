document.addEventListener("mousemove", (e) => {
    const x = e.clientX;
    const y = e.clientY;
    document.body.style.background = `radial-gradient(circle closest-side at ${x}px ${y}px, #B0E0E6, #d5f8f9)`;
});
