/* === INLINE EDITOR: LOCAL DRAFTS AND PORTABLE HTML EXPORT === */
class InlineEditor {
  constructor() {
    this.active = false;
    this.key = "yukuan-intro-ivory-v1:" + location.pathname;
    this.nodes = [...document.querySelectorAll("[data-edit]")];
    this.key +=
      ":" +
      this.nodes.reduce((hash, node) => {
        for (const char of node.textContent)
          hash = (Math.imul(hash, 31) + char.charCodeAt(0)) | 0;
        return hash;
      }, 0);
    this.bar = document.querySelector(".editor-bar");
    this.status = document.querySelector("#editStatus");
    this.nodes.forEach((n, i) => {
      n.dataset.editId = String(i);
      n.addEventListener("input", () => this.persist());
      n.addEventListener("paste", (e) => {
        e.preventDefault();
        document.execCommand(
          "insertText",
          false,
          e.clipboardData.getData("text/plain"),
        );
      });
    });
    try {
      const saved = JSON.parse(localStorage.getItem(this.key) || "null");
      if (saved)
        this.nodes.forEach((n, i) => {
          if (typeof saved[i] === "string") n.textContent = saved[i];
        });
    } catch {}
    document.querySelector("#editToggle").onclick = () => this.toggle();
    document.querySelector("#saveFile").onclick = () => this.save();
    const zone = document.querySelector(".edit-hotzone");
    let timer;
    for (const el of [zone, this.bar]) {
      el.addEventListener("mouseenter", () => {
        clearTimeout(timer);
        this.bar.classList.add("show");
      });
      el.addEventListener("mouseleave", () => {
        timer = setTimeout(() => {
          if (!this.active) this.bar.classList.remove("show");
        }, 400);
      });
    }
    zone.onclick = () => this.toggle();
  }
  toggle() {
    this.active = !this.active;
    document.body.classList.toggle("editing", this.active);
    this.bar.classList.toggle("active", this.active);
    this.nodes.forEach((n) =>
      n.setAttribute("contenteditable", String(this.active)),
    );
    document.querySelector("#editToggle").textContent = this.active
      ? "Done (Esc)"
      : "Edit (E)";
    this.status.textContent = this.active ? "Click text to edit" : "";
    if (!this.active) {
      document.activeElement.blur();
      this.bar.classList.remove("show");
    }
  }
  persist() {
    try {
      localStorage.setItem(
        this.key,
        JSON.stringify(this.nodes.map((n) => n.textContent)),
      );
      this.status.textContent = "Saved locally";
    } catch {
      this.status.textContent = "Use Save HTML";
    }
    requestAnimationFrame(() => {
      let overflow = false;
      this.nodes.forEach((n) => {
        const bad =
          n.scrollWidth > n.clientWidth + 2 &&
          getComputedStyle(n).display !== "inline";
        n.toggleAttribute("data-overflow", bad);
        overflow ||= bad;
      });
      if (overflow) this.status.textContent = "Text too wide — shorten";
    });
  }
  save() {
    const clone = document.documentElement.cloneNode(true);
    clone.querySelector("body").classList.remove("editing");
    clone.querySelector(".editor-bar").classList.remove("active", "show");
    clone.querySelector("#editToggle").textContent = "Edit (E)";
    clone.querySelector("#editStatus").textContent = "";
    clone.querySelectorAll("[data-edit]").forEach((n) => {
      n.removeAttribute("contenteditable");
      n.removeAttribute("data-overflow");
    });
    clone.querySelectorAll(".slide").forEach((s, i) => {
      s.classList.toggle("active", i === 0);
      s.classList.toggle("visible", i === 0);
      s.setAttribute("aria-hidden", String(i !== 0));
      s.inert = i !== 0;
    });
    const blob = new Blob(["<!doctype html>" + clone.outerHTML], {
      type: "text/html",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "yukuan-lu-world-models.html";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 3000);
    this.status.textContent = "HTML downloaded";
  }
}
