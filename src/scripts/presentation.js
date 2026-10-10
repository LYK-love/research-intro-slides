class SlidePresentation {
  constructor(editor) {
    this.editor = editor;
    this.slides = [...document.querySelectorAll(".slide")];
    this.currentSlide = 0;
    this.stage = document.querySelector(".deck-stage");
    this.scale();
    addEventListener("resize", () => this.scale());
    this.showSlide(Number(location.hash.slice(1)) - 1 || 0);
    addEventListener("hashchange", () =>
      this.showSlide(Number(location.hash.slice(1)) - 1 || 0),
    );
    this.bindNavigation();
  }
  scale() {
    const s = Math.min(innerWidth / 1920, innerHeight / 1080);
    this.stage.style.transform = `translate(${(innerWidth - 1920 * s) / 2}px,${(innerHeight - 1080 * s) / 2}px) scale(${s})`;
  }
  showSlide(n) {
    this.currentSlide = Math.max(0, Math.min(n, this.slides.length - 1));
    this.slides.forEach((s, i) => {
      const active = i === this.currentSlide;
      s.classList.toggle("active", active);
      s.classList.toggle("visible", active);
      s.setAttribute("aria-hidden", String(!active));
      s.inert = !active;
    });
    try {
      history.replaceState(null, "", "#" + (this.currentSlide + 1));
    } catch {}
  }
  bindNavigation() {
    addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
        e.preventDefault();
        this.editor.save();
        return;
      }
      if (e.key === "Escape" && this.editor.active) {
        this.editor.toggle();
        return;
      }
      if (e.target.isContentEditable || e.target.closest("button")) return;
      if (e.key.toLowerCase() === "e" && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        this.editor.toggle();
        return;
      }
      if (this.editor.active) return;
      let n = this.currentSlide;
      if (["ArrowRight", "ArrowDown", " ", "PageDown"].includes(e.key)) n++;
      else if (["ArrowLeft", "ArrowUp", "PageUp"].includes(e.key)) n--;
      else if (e.key === "Home") n = 0;
      else if (e.key === "End") n = this.slides.length - 1;
      else return;
      e.preventDefault();
      this.showSlide(n);
    });
    let last = 0,
      acc = 0;
    addEventListener(
      "wheel",
      (e) => {
        if (this.editor.active || e.ctrlKey) return;
        e.preventDefault();
        if (Date.now() - last < 700) return;
        acc += Math.abs(e.deltaY) > Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
        if (Math.abs(acc) > 45) {
          this.showSlide(this.currentSlide + Math.sign(acc));
          acc = 0;
          last = Date.now();
        }
      },
      { passive: false },
    );
    let start = null;
    this.stage.addEventListener(
      "touchstart",
      (e) => {
        if (
          this.editor.active ||
          e.target.closest("a") ||
          e.touches.length !== 1
        )
          return;
        start = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      },
      { passive: true },
    );
    this.stage.addEventListener(
      "touchend",
      (e) => {
        if (!start || this.editor.active) return;
        const dx = e.changedTouches[0].clientX - start.x,
          dy = e.changedTouches[0].clientY - start.y;
        if (Math.abs(dx) > 35 && Math.abs(dx) > Math.abs(dy))
          this.showSlide(this.currentSlide + (dx < 0 ? 1 : -1));
        start = null;
      },
      { passive: true },
    );
  }
}
const editor = new InlineEditor();
window.presentation = new SlidePresentation(editor);
