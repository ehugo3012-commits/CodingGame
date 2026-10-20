// Tiny Markdown renderer + syntax highlighter (no dependencies, works offline).

export function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ------------------------------------------------------------ highlighter
const PY_KW = new Set(("False None True and as assert async await break class continue def del elif else except " +
  "finally for from global if import in is lambda nonlocal not or pass raise return try while with yield match case").split(" "));
const PY_BUILTIN = new Set(("print input int float str list dict set tuple len range sum min max abs sorted reversed " +
  "enumerate zip map filter any all open round pow divmod isinstance type bool chr ord bin hex oct sys math self").split(" "));
const CPP_KW = new Set(("alignas auto bool break case catch char class const constexpr continue default delete do double " +
  "else enum explicit extern false float for friend goto if inline int long mutable namespace new noexcept nullptr " +
  "operator private protected public return short signed sizeof static static_cast struct switch template this throw " +
  "true try typedef typename union unsigned using virtual void volatile while size_t").split(" "));
const CPP_TYPES = new Set(("std string vector map set unordered_map unordered_set pair tuple queue stack deque " +
  "priority_queue array cin cout cerr endl getline sort swap min max abs make_pair unique_ptr shared_ptr " +
  "greater less accumulate reverse lower_bound upper_bound int64_t uint64_t").split(" "));

const TOKEN_RE = {
  python: /(#[^\n]*)|("""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|[rRbBfF]{0,2}"(?:\\.|[^"\\\n])*"?|[rRbBfF]{0,2}'(?:\\.|[^'\\\n])*'?)|(\b\d[\d_]*\.?\d*(?:[eE][+-]?\d+)?j?\b|\b0[xXoObB][\da-fA-F_]+\b)|([A-Za-z_]\w*)/g,
  cpp: /(\/\/[^\n]*|\/\*[\s\S]*?(?:\*\/|$))|("(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?)|(\b\d[\d']*\.?\d*(?:[eE][+-]?\d+)?[uUlLfF]*\b|\b0[xX][\da-fA-F']+\b)|(#\s*\w+|[A-Za-z_]\w*)/g,
};

export function highlight(code, lang) {
  const re = TOKEN_RE[lang === "cpp" ? "cpp" : "python"];
  const kw = lang === "cpp" ? CPP_KW : PY_KW;
  const builtins = lang === "cpp" ? CPP_TYPES : PY_BUILTIN;
  let out = "";
  let last = 0;
  re.lastIndex = 0;
  let m;
  while ((m = re.exec(code))) {
    out += esc(code.slice(last, m.index));
    const [tok, com, str, num, word] = m;
    let cls = null;
    if (com) cls = "com";
    else if (str) cls = "str";
    else if (num) cls = "num";
    else if (word) {
      if (word[0] === "#") cls = "pre";
      else if (kw.has(word)) cls = "kw";
      else if (builtins.has(word)) cls = "ty";
      else if (code[re.lastIndex] === "(") cls = "fn";
    }
    out += cls ? `<span class="tok-${cls}">${esc(tok)}</span>` : esc(tok);
    last = re.lastIndex;
    if (tok.length === 0) re.lastIndex++;
  }
  return out + esc(code.slice(last));
}

export function codeBlock(code, lang) {
  return `<pre class="codeblock"><code>${highlight(code, lang)}</code></pre>`;
}

// --------------------------------------------------------------- markdown
function inline(text) {
  const codes = [];
  let s = text.replace(/`([^`]+)`/g, (_, c) => {
    codes.push(c);
    return `\u0000${codes.length - 1}\u0000`;
  });
  s = esc(s)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*\w])\*(\S(?:[^*\n]*\S)?)\*(?!\w)/g, "$1<em>$2</em>")
    .replace(/(^|[^_\w])_(\S(?:[^_\n]*\S)?)_(?!\w)/g, "$1<em>$2</em>")
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  return s.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${esc(codes[+i])}</code>`);
}

export function markdown(src, defaultLang = "python") {
  const lines = String(src || "").replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let i = 0;
  const isBlockStart = (l) => /^(```|#{1,4}\s|>\s?|\s*[-*]\s+|\s*\d+[.)]\s+|\|)/.test(l);
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    const fence = line.match(/^```\s*(\w*)/);
    if (fence) {
      const lang = fence[1] || defaultLang;
      const body = [];
      i++;
      while (i < lines.length && !lines[i].startsWith("```")) body.push(lines[i++]);
      i++;
      const code = body.join("\n");
      out.push(["python", "py", "cpp", "c++", "c"].includes(lang.toLowerCase())
        ? codeBlock(code, lang.startsWith("py") ? "python" : "cpp")
        : `<pre class="codeblock"><code>${esc(code)}</code></pre>`);
      continue;
    }
    const h = line.match(/^(#{1,4})\s+(.*)/);
    if (h) {
      const lvl = Math.min(h[1].length + 1, 4);
      out.push(`<h${lvl}>${inline(h[2])}</h${lvl}>`);
      i++;
      continue;
    }
    if (/^>\s?/.test(line)) {
      const body = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) body.push(lines[i++].replace(/^>\s?/, ""));
      out.push(`<blockquote>${markdown(body.join("\n"), defaultLang)}</blockquote>`);
      continue;
    }
    if (/^\s*[-*]\s+/.test(line) || /^\s*\d+[.)]\s+/.test(line)) {
      const ordered = /^\s*\d+[.)]\s+/.test(line);
      const items = [];
      while (i < lines.length && (ordered ? /^\s*\d+[.)]\s+/ : /^\s*[-*]\s+/).test(lines[i])) {
        let item = lines[i++].replace(/^\s*(?:[-*]|\d+[.)])\s+/, "");
        while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !/^\s*(?:[-*]|\d+[.)])\s+/.test(lines[i])) {
          item += " " + lines[i++].trim();
        }
        items.push(`<li>${inline(item)}</li>`);
      }
      out.push(ordered ? `<ol>${items.join("")}</ol>` : `<ul>${items.join("")}</ul>`);
      continue;
    }
    if (/^\|/.test(line)) {
      const rows = [];
      while (i < lines.length && /^\|/.test(lines[i])) rows.push(lines[i++]);
      // Split on | but not inside `code` spans (so `a || b` works in a cell).
      const cells = (r) => {
        const out = [""];
        let inCode = false;
        for (const ch of r.trim().replace(/^\||\|$/g, "")) {
          if (ch === "`") inCode = !inCode;
          if (ch === "|" && !inCode) out.push("");
          else out[out.length - 1] += ch;
        }
        return out.map((c) => c.trim());
      };
      const head = cells(rows[0]);
      const body = rows.slice(/^\|[\s:|-]+\|?$/.test(rows[1] || "") ? 2 : 1);
      out.push(`<table><thead><tr>${head.map((c) => `<th>${inline(c)}</th>`).join("")}</tr></thead><tbody>` +
        body.map((r) => `<tr>${cells(r).map((c) => `<td>${inline(c)}</td>`).join("")}</tr>`).join("") +
        "</tbody></table>");
      continue;
    }
    const para = [];
    while (i < lines.length && lines[i].trim() && !(para.length && isBlockStart(lines[i]))) para.push(lines[i++]);
    out.push(`<p>${inline(para.join(" "))}</p>`);
  }
  return out.join("\n");
}
