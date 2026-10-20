// Mobile-friendly code editor: textarea + highlighted overlay + symbol key bar.
//
// Phone keyboards make symbols like { } [ ] ; painful, so - like Termux's
// extra-keys row - we put them one tap away. Auto-indent follows Python's
// ":" and C++'s "{" conventions.

import { highlight } from "./md.js";

const KEYS = {
  python: ["⇥", ":", "(", ")", "[", "]", "{", "}", "=", '"', "'", "#", ".", ",", "+", "-", "*", "/", "%", "<", ">", "_", "!", "&", "|", "←", "→", "↶"],
  cpp: ["⇥", ";", "{", "}", "(", ")", "[", "]", "<", ">", "=", '"', "'", "&", "*", ":", "#", ".", ",", "+", "-", "/", "%", "!", "|", "_", "←", "→", "↶"],
};
const INDENT = "    ";

export function createEditor(host, { lang = "python", value = "", onChange, fontSize } = {}) {
  host.innerHTML = `
    <div class="editor">
      <div class="gutter" aria-hidden="true"></div>
      <div class="layer">
        <pre class="hl" aria-hidden="true"><code></code></pre>
        <textarea class="code" spellcheck="false" autocapitalize="off" autocomplete="off"
          autocorrect="off" wrap="off" aria-label="Code editor"></textarea>
      </div>
    </div>
    <div class="keybar" role="toolbar" aria-label="Symbols"></div>`;
  const wrap = host.querySelector(".editor");
  const ta = host.querySelector("textarea");
  const hl = host.querySelector("pre.hl code");
  const pre = host.querySelector("pre.hl");
  const gutter = host.querySelector(".gutter");
  const keybar = host.querySelector(".keybar");
  if (fontSize) wrap.style.setProperty("--code-size", `${fontSize}px`);

  let curLang = lang;
  let changeTimer = null;

  function render() {
    const v = ta.value;
    hl.innerHTML = highlight(v, curLang) + "\n";
    const n = v.split("\n").length;
    gutter.textContent = Array.from({ length: n }, (_, i) => i + 1).join("\n");
    ta.style.height = "auto";
    ta.style.height = Math.max(260, ta.scrollHeight + 2) + "px";
    pre.scrollLeft = ta.scrollLeft;
  }

  function changed() {
    render();
    if (onChange) {
      clearTimeout(changeTimer);
      changeTimer = setTimeout(() => onChange(ta.value), 800);
    }
  }

  function insert(text) {
    ta.focus();
    // execCommand keeps the native undo stack working; fall back if unsupported.
    if (!document.execCommand || !document.execCommand("insertText", false, text)) {
      ta.setRangeText(text, ta.selectionStart, ta.selectionEnd, "end");
    }
    changed();
  }

  function lineBeforeCaret() {
    const v = ta.value;
    const start = v.lastIndexOf("\n", ta.selectionStart - 1) + 1;
    return v.slice(start, ta.selectionStart);
  }

  function newline() {
    const before = lineBeforeCaret();
    let indent = before.match(/^[ \t]*/)[0];
    const trimmed = before.trimEnd();
    if ((curLang === "python" && trimmed.endsWith(":")) || (curLang === "cpp" && /[{(\[]$/.test(trimmed))) {
      indent += INDENT;
    }
    const after = ta.value.slice(ta.selectionEnd);
    if (curLang === "cpp" && trimmed.endsWith("{") && after.startsWith("}")) {
      // Typing Enter between {} -> put the brace on its own dedented line.
      const outer = indent.slice(INDENT.length);
      insert("\n" + indent + "\n" + outer);
      const pos = ta.selectionStart - outer.length - 1;
      ta.setSelectionRange(pos, pos);
      return;
    }
    insert("\n" + indent);
  }

  function closeBrace(ch) {
    const before = lineBeforeCaret();
    if (/^ +$/.test(before)) {
      const remove = Math.min(INDENT.length, before.length);
      ta.setSelectionRange(ta.selectionStart - remove, ta.selectionEnd);
    }
    insert(ch);
  }

  function smartBackspace() {
    const before = lineBeforeCaret();
    if (ta.selectionStart === ta.selectionEnd && before.length && /^ +$/.test(before)) {
      const remove = before.length % INDENT.length || INDENT.length;
      ta.setSelectionRange(ta.selectionStart - remove, ta.selectionStart);
      insert("");
      return true;
    }
    return false;
  }

  ta.addEventListener("keydown", (e) => {
    if (e.isComposing) return;
    if (e.key === "Tab") {
      e.preventDefault();
      insert(INDENT);
    } else if (e.key === "Enter" && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      newline();
    } else if (e.key === "Backspace" && smartBackspace()) {
      e.preventDefault();
    } else if (e.key === "}" && curLang === "cpp") {
      e.preventDefault();
      closeBrace("}");
    }
  });
  // Android soft keyboards often don't report keydown for Enter; beforeinput is reliable.
  ta.addEventListener("beforeinput", (e) => {
    if (e.inputType === "insertLineBreak" || e.inputType === "insertParagraph") {
      e.preventDefault();
      newline();
    }
  });
  ta.addEventListener("input", changed);
  ta.addEventListener("scroll", () => { pre.scrollLeft = ta.scrollLeft; });

  function buildKeys() {
    keybar.innerHTML = "";
    for (const k of KEYS[curLang] || KEYS.python) {
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = k;
      b.setAttribute("aria-label", { "⇥": "Tab", "←": "Cursor left", "→": "Cursor right", "↶": "Undo" }[k] || k);
      // pointerdown + preventDefault keeps the soft keyboard open.
      b.addEventListener("pointerdown", (e) => e.preventDefault());
      b.addEventListener("click", () => {
        if (k === "⇥") insert(INDENT);
        else if (k === "←" || k === "→") {
          ta.focus();
          const p = Math.max(0, Math.min(ta.value.length, ta.selectionStart + (k === "←" ? -1 : 1)));
          ta.setSelectionRange(p, p);
        } else if (k === "↶") {
          ta.focus();
          document.execCommand("undo");
          changed();
        } else if (k === "}" && curLang === "cpp") closeBrace("}");
        else insert(k);
      });
      keybar.appendChild(b);
    }
  }

  ta.value = value;
  buildKeys();
  requestAnimationFrame(render);

  return {
    el: wrap,
    textarea: ta,
    getValue: () => ta.value,
    setValue(v) {
      ta.value = v;
      render();
    },
    setLang(l) {
      curLang = l;
      buildKeys();
      render();
    },
    flush() {
      if (changeTimer && onChange) {
        clearTimeout(changeTimer);
        changeTimer = null;
        onChange(ta.value);
      }
    },
    focus: () => ta.focus(),
  };
}
