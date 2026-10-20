// CodeQuest single-page app: hash router + views.
import { api } from "./api.js";
import { createEditor } from "./editor.js";
import { codeBlock, esc, markdown } from "./md.js";

const view = document.getElementById("view");
const titleEl = document.getElementById("page-title");
const backBtn = document.getElementById("back-btn");
const LANG_NAME = { python: "Python", cpp: "C++" };
const DIFF_LABEL = { beginner: "Beginner", easy: "Easy", medium: "Medium", hard: "Hard", expert: "Expert" };

const state = { settings: null, health: null, cleanup: null, codingView: false };

// ----------------------------------------------------------------- helpers
const $ = (sel, root = view) => root.querySelector(sel);
const $$ = (sel, root = view) => Array.from(root.querySelectorAll(sel));

function storage(key, value) {
  try {
    if (value === undefined) return JSON.parse(localStorage.getItem(key) || "null");
    localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    return null;
  }
  return value;
}

let toastTimer;
function toast(msg, isError = false) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = "show" + (isError ? " error" : "");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (t.className = ""), isError ? 5000 : 2600);
}

function setTitle(text, back = null) {
  titleEl.textContent = text;
  document.title = text === "CodeQuest" ? "CodeQuest" : `${text} · CodeQuest`;
  backBtn.hidden = !back;
  backBtn.onclick = () => (history.length > 1 ? history.back() : (location.hash = back));
}

function setTab(name) {
  document.querySelectorAll(".tabbar a").forEach((a) => a.classList.toggle("active", a.dataset.tab === name));
}

function updateTopbar(level, streak) {
  if (!level) return;
  document.getElementById("topbar-stats").innerHTML =
    `<span title="Streak">🔥 <b>${streak ?? 0}</b></span><span title="Level">⭐ <b>${level.level}</b></span>`;
}

function diffBadge(d) {
  return `<span class="badge-diff d-${d}">${DIFF_LABEL[d] || d}</span>`;
}

function loading() {
  view.innerHTML = `<div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div>`;
}

function errorView(err) {
  view.innerHTML = `<div class="card"><h3>Something went wrong</h3><p class="muted">${esc(err.message)}</p>
    <button class="btn" onclick="location.reload()">Retry</button></div>`;
}

function spinBtn(btn, on) {
  if (on) {
    btn.dataset.label = btn.innerHTML;
    btn.innerHTML = `<span class="spinner"></span>`;
    btn.disabled = true;
  } else {
    btn.innerHTML = btn.dataset.label || btn.innerHTML;
    btn.disabled = false;
  }
}

function modal(html) {
  const root = document.getElementById("modal-root");
  root.innerHTML = `<div class="modal-backdrop"><div class="modal" role="dialog" aria-modal="true">${html}</div></div>`;
  const close = () => (root.innerHTML = "");
  root.querySelector(".modal-backdrop").addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-backdrop") || e.target.closest("[data-close]")) close();
  });
  return { root, close };
}

// window.confirm() is a no-op in the APK's WebView (no WebChromeClient), so use our own.
function confirmDialog(message, okLabel = "OK") {
  return new Promise((resolve) => {
    const m = modal(`<p>${esc(message)}</p><div class="row mt">
      <button class="btn grow" data-close data-v="0">Cancel</button>
      <button class="btn primary grow" data-close data-v="1">${esc(okLabel)}</button></div>`);
    m.root.querySelectorAll("[data-v]").forEach((b) => b.addEventListener("click", () => resolve(b.dataset.v === "1")));
    m.root.querySelector(".modal-backdrop").addEventListener("click", (e) => {
      if (e.target.classList.contains("modal-backdrop")) resolve(false);
    });
  });
}

function confetti() {
  const box = document.createElement("div");
  box.className = "confetti";
  const colors = ["#7c5cff", "#20c4a7", "#ffe066", "#ff5c7a", "#3ddc84", "#82aaff"];
  for (let i = 0; i < 70; i++) {
    const p = document.createElement("i");
    p.style.left = Math.random() * 100 + "vw";
    p.style.background = colors[i % colors.length];
    p.style.animationDuration = 1.6 + Math.random() * 1.8 + "s";
    p.style.animationDelay = Math.random() * 0.4 + "s";
    box.appendChild(p);
  }
  document.body.appendChild(box);
  setTimeout(() => box.remove(), 4000);
}

function celebrate(reward, { title = "Accepted!", subtitle = "" } = {}) {
  if (!reward) return;
  updateTopbar(reward.level, reward.streak);
  const gained = reward.xp || 0;
  if (!gained && !(reward.new_badges || []).length) return;
  confetti();
  const badges = (reward.new_badges || [])
    .map((b) => `<div class="badge"><div class="bi">${b.icon}</div><div class="bn">${esc(b.name)}</div>
      <div class="bd">${esc(b.description)}</div></div>`).join("");
  const lv = reward.level;
  modal(`
    <div class="big">🎉</div>
    <h2>${esc(title)}</h2>
    ${subtitle ? `<p class="muted">${esc(subtitle)}</p>` : ""}
    <div class="xp-gain">+${gained} XP</div>
    <p class="muted small">Level ${lv.level} · ${esc(lv.title)} — ${lv.xp} / ${lv.level_end} XP</p>
    <div class="progress"><i style="width:${Math.round(lv.progress * 100)}%"></i></div>
    <p class="small">🔥 Streak: <b>${reward.streak}</b> day${reward.streak === 1 ? "" : "s"}</p>
    ${badges ? `<h3 class="mt">New badge${reward.new_badges.length > 1 ? "s" : ""}!</h3><div class="badges">${badges}</div>` : ""}
    <button class="btn primary block mt" data-close>Keep going</button>`);
}

// ------------------------------------------------------------ time tracker
// Counts *active* minutes in coding views (lessons, problems, playground):
// app visible + the learner touched/typed within the last 2 minutes.
const tracker = { lastInteract: Date.now(), pending: 0 };
["pointerdown", "keydown", "input", "scroll", "touchstart"].forEach((ev) =>
  addEventListener(ev, () => (tracker.lastInteract = Date.now()), { passive: true, capture: true }));
setInterval(() => {
  if (document.visibilityState !== "visible" || !state.codingView) return;
  if (Date.now() - tracker.lastInteract > 120000) return;
  tracker.pending += 5;
  if (tracker.pending >= 30) flushTracker();
}, 5000);
function flushTracker() {
  const s = tracker.pending;
  if (!s) return;
  tracker.pending = 0;
  fetch("/api/heartbeat", {
    method: "POST", keepalive: true,
    headers: { "Content-Type": "application/json", "X-TZ-Offset": String(new Date().getTimezoneOffset()) },
    body: JSON.stringify({ seconds: s }),
  }).catch(() => (tracker.pending += s));
}
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") flushTracker();
});

// Hide the tab bar while typing so the soft keyboard has room.
document.addEventListener("focusin", (e) => {
  if (e.target.matches("textarea, input")) document.body.classList.add("editing");
});
document.addEventListener("focusout", () => setTimeout(() => {
  if (!document.activeElement || !document.activeElement.matches("textarea, input")) {
    document.body.classList.remove("editing");
  }
}, 100));

// ------------------------------------------------------------ result views
function testDots(tests) {
  return `<div class="test-dots">${tests.map((t) => {
    const cls = t.verdict === "ok" ? "ok" : t.verdict === "skipped" ? "skip" : "bad";
    return `<span class="${cls}" title="${t.kind} test ${t.index}: ${t.verdict}">${t.index}</span>`;
  }).join("")}</div>`;
}

const VERDICT_TEXT = {
  ok: "Passed", wrong: "Wrong answer", error: "Runtime error", timeout: "Time limit exceeded",
  output_limit: "Output limit exceeded", compile_error: "Compilation error", skipped: "Skipped",
};

function resultHtml(res, { submit }) {
  if (res.compile_error) {
    return `<div class="verdict bad">⚠️ Compilation Error</div>
      <div class="output err">${esc(res.compile_error)}</div>`;
  }
  const ok = res.verdict === "ok";
  const firstBad = res.tests.find((t) => t.verdict !== "ok");
  const label = ok ? (submit ? "✅ Accepted" : "✅ Samples pass") :
    `❌ ${res.verdict_text}${firstBad ? ` <small>on ${firstBad.kind} test ${firstBad.index}</small>` : ""}`;
  let html = `<div class="verdict ${ok ? "ok" : "bad"}"><span>${label}</span><small>${res.passed}/${res.total}</small></div>`;
  html += testDots(res.tests);
  if (ok && !submit) html += `<p class="small muted">Samples pass! Submit to run the hidden tests.</p>`;
  for (const t of res.tests) {
    const show = t.kind === "sample" || (t.verdict !== "ok" && t === firstBad);
    if (!show) continue;
    const open = t === firstBad ? "open" : "";
    html += `<details class="test" ${open}><summary>${t.kind === "sample" ? "Sample" : "Hidden"} test ${t.index} —
      <span style="color:var(${t.verdict === "ok" ? "--ok" : "--bad"})">${VERDICT_TEXT[t.verdict] || t.verdict}</span>
      <span class="muted small">${t.time.toFixed(3)}s</span></summary>`;
    if (t.kind === "sample") {
      html += `<div class="io-label">Input</div><div class="output">${esc(t.input) || "<i>(empty)</i>"}</div>
        <div class="io-label">Expected output</div><div class="output">${esc(t.expected)}</div>
        <div class="io-label">Your output</div><div class="output">${esc(t.output) || "<i>(nothing printed)</i>"}</div>`;
    } else {
      html += `<p class="small muted">Hidden tests don't reveal their data — re-read the constraints and think about edge cases
        (empty input, minimum/maximum values, duplicates, negative numbers, overflow).</p>`;
    }
    if (t.error) html += `<div class="io-label">Error</div><div class="output err">${esc(t.error)}</div>`;
    if (t.stderr) html += `<div class="io-label">stderr</div><div class="output">${esc(t.stderr)}</div>`;
    html += `</details>`;
  }
  return html;
}

function customRunHtml(r) {
  const bad = r.status !== "ok";
  let html = `<div class="verdict ${bad ? "bad" : "ok"}"><span>${bad ? "⚠️ " + (VERDICT_TEXT[r.status] || r.status) : "▶ Finished"}</span>
    <small>${(r.time || 0).toFixed(3)}s</small></div>`;
  html += `<div class="io-label">Output</div><div class="output">${esc(r.stdout) || "<i>(nothing printed)</i>"}</div>`;
  if (r.stderr) html += `<div class="io-label">stderr</div><div class="output">${esc(r.stderr)}</div>`;
  if (r.error) html += `<div class="io-label">Error</div><div class="output err">${esc(r.error)}</div>`;
  return html;
}

function solutionHtml(solution, current) {
  if (!solution) return "";
  return Object.entries(solution).map(([lang, code]) => `
    <details class="test" ${lang === current ? "" : ""}><summary>📖 Reference solution (${LANG_NAME[lang]})</summary>
      ${codeBlock(code, lang)}</details>`).join("");
}

// ---------------------------------------------------------------- views
async function homeView() {
  setTitle("CodeQuest");
  setTab("home");
  const d = await api.home();
  updateTopbar(d.level, d.streak.current);
  const lv = d.level;
  const pct = Math.min(100, Math.round((d.time.today_minutes / Math.max(1, d.time.goal_minutes)) * 100));
  const cont = (track) => {
    const c = d.continue[track];
    if (!c.total) return "";
    const p = Math.round((c.done / c.total) * 100);
    const next = c.next
      ? `<a class="btn primary small" href="#/lesson/${c.next.id}">Continue</a>`
      : `<span class="small" style="color:var(--ok)">Track complete ✓</span>`;
    return `<div class="list-item"><div class="check ${c.done === c.total ? "done" : ""}">${track === "python" ? "🐍" : "⚡"}</div>
      <div class="grow"><div><b>${LANG_NAME[track]} track</b> <span class="muted small">${c.done}/${c.total}</span></div>
      <div class="small muted">${c.next ? esc(c.next.unit + " · " + c.next.title) : "All lessons done"}</div>
      <div class="progress mt"><i style="width:${p}%"></i></div></div>${next}</div>`;
  };
  view.innerHTML = `
    <div class="card hero">
      <div class="row">
        <div class="level-badge">${lv.level}</div>
        <div class="grow">
          <div style="font-weight:800;font-size:18px">${esc(lv.title)}</div>
          <div class="muted small">${lv.xp} XP · ${lv.level_end - lv.xp} XP to level ${lv.level + 1}</div>
          <div class="progress mt"><i style="width:${Math.round(lv.progress * 100)}%"></i></div>
        </div>
      </div>
    </div>
    <div class="stat-grid">
      <div class="stat"><div class="v">🔥 ${d.streak.current}</div><div class="k">Day streak</div></div>
      <div class="stat"><div class="row" style="justify-content:center"><div class="ring" style="--p:${pct}"><span>${Math.round(d.time.today_minutes)}m</span></div></div>
        <div class="k">of ${d.time.goal_minutes}m goal</div></div>
      <div class="stat"><div class="v">${d.solved}</div><div class="k">of ${d.total_problems} solved</div></div>
    </div>
    ${d.streak.active_today ? "" : `<p class="small muted center">${d.streak.current ? "Solve a problem or finish a lesson today to keep your streak alive!" : "Earn XP today to start a streak."}</p>`}
    <div class="section-title">Continue learning</div>
    <div class="list">${cont("python")}${cont("cpp")}</div>
    ${d.daily ? `<div class="section-title">Problem of the day</div>
      <a class="list-item list" href="#/problem/${d.daily.id}">
        <div class="check">🎯</div>
        <div class="grow"><b>${esc(d.daily.title)}</b><div class="row small mt">${diffBadge(d.daily.difficulty)}
          <span class="tag">${esc(d.daily.category)}</span><span class="muted">+${d.daily.xp} XP</span></div></div>
        <span class="muted">›</span></a>` : ""}
    <div class="section-title">Quick start</div>
    <div class="quick">
      <a class="btn" href="#/practice"><span>🧩</span>Practice</a>
      <a class="btn" href="#/play"><span>⌨️</span>Playground</a>
      <a class="btn" href="#/profile"><span>🏆</span>${d.badges_earned} badges</a>
    </div>`;
}

async function learnView({ track }) {
  track = track === "cpp" ? "cpp" : "python";
  setTitle("Learn");
  setTab("learn");
  const d = await api.lessons(track);
  const total = d.units.reduce((n, u) => n + u.lessons.length, 0);
  const done = d.units.reduce((n, u) => n + u.lessons.filter((l) => l.done).length, 0);
  view.innerHTML = `
    <div class="seg" id="track-seg">
      <button data-t="python" class="${track === "python" ? "on" : ""}">🐍 Python</button>
      <button data-t="cpp" class="${track === "cpp" ? "on" : ""}">⚡ C++</button>
    </div>
    <div class="card mt"><div class="spread"><b>${LANG_NAME[track]} track</b><span class="muted small">${done}/${total} lessons</span></div>
      <div class="progress mt"><i style="width:${total ? Math.round((done / total) * 100) : 0}%"></i></div></div>
    ${d.units.map((u, ui) => `
      <div class="section-title">Unit ${ui + 1} · ${esc(u.name)}</div>
      <div class="list">${u.lessons.map((l) => `
        <a class="list-item" href="#/lesson/${l.id}">
          <div class="check ${l.done ? "done" : ""}">${l.done ? "✓" : ""}</div>
          <div class="grow"><b>${esc(l.title)}</b><div class="small muted">${esc(l.summary)}</div></div>
          ${l.has_challenge ? `<span title="Includes a coding challenge">🧪</span>` : ""}
          <span class="muted">›</span></a>`).join("")}
      </div>`).join("") || `<div class="card muted">No lessons yet.</div>`}`;
  $$("#track-seg button").forEach((b) => b.addEventListener("click", () => (location.hash = `#/learn/${b.dataset.t}`)));
}

async function lessonView({ id }) {
  state.codingView = true;
  const l = await api.lesson(id);
  setTitle(l.title, `#/learn/${l.track}`);
  setTab("learn");
  const lang = l.track;
  view.innerHTML = `
    <div class="muted small">${LANG_NAME[lang]} · ${esc(l.unit)} · Lesson ${l.position[0]} of ${l.position[1]}
      ${l.done ? ` · <span style="color:var(--ok)">Completed ✓</span>` : ` · +${l.xp} XP`}</div>
    <h2 style="margin:6px 0 12px">${esc(l.title)}</h2>
    <div class="card md">${markdown(l.body, lang)}</div>
    ${l.examples.length ? `<div class="section-title">Try it</div>` : ""}
    ${l.examples.map((ex, i) => `
      <div class="card" data-ex="${i}">
        <div class="spread"><b>${esc(ex.title)}</b></div>
        ${ex.explain ? `<div class="md small muted">${markdown(ex.explain, lang)}</div>` : ""}
        <div class="mt">${codeBlock(ex.code, lang)}</div>
        ${ex.stdin ? `<div class="io-label">Input</div><div class="output">${esc(ex.stdin)}</div>` : ""}
        <div class="toolbar"><button class="btn small" data-run="${i}">▶ Run</button>
          <button class="btn small ghost" data-edit="${i}">✎ Edit in playground</button></div>
        <div class="ex-out"></div>
      </div>`).join("")}
    ${l.challenge ? `
      <div class="section-title">Your turn 🧪</div>
      <div class="card">
        <div class="md">${markdown(l.challenge.prompt, lang)}</div>
        ${l.challenge.samples.map((s) => `<div class="two-col"><div><div class="io-label">Sample input</div>
          <div class="output">${esc(s.input) || "<i>(none)</i>"}</div></div><div><div class="io-label">Expected output</div>
          <div class="output">${esc(s.output)}</div></div></div>`).join("")}
        <div class="mt" id="ch-editor"></div>
        <div class="toolbar"><button class="btn" id="ch-run">▶ Run</button>
          <button class="btn go" id="ch-submit">${l.done ? "✓ Submit again" : "🚀 Submit"}</button></div>
        <div id="ch-result" class="mt"></div>
        <div id="ch-solution">${l.challenge.solution ? solutionHtml({ [lang]: l.challenge.solution }) : ""}</div>
      </div>` : `
      <div class="mt">${l.done ? `<div class="verdict ok">✓ Lesson completed</div>` :
        `<button class="btn go block" id="mark-done">✓ Mark lesson complete (+${l.xp} XP)</button>`}</div>`}
    <div class="row mt">
      ${l.prev ? `<a class="btn grow" href="#/lesson/${l.prev}">‹ Previous</a>` : `<span class="grow"></span>`}
      ${l.next ? `<a class="btn primary grow" href="#/lesson/${l.next}">Next ›</a>` :
        `<a class="btn primary grow" href="#/practice">Practice problems ›</a>`}
    </div>`;

  $$("[data-run]").forEach((btn) => btn.addEventListener("click", async () => {
    const ex = l.examples[+btn.dataset.run];
    const out = btn.closest(".card").querySelector(".ex-out");
    spinBtn(btn, true);
    try {
      out.innerHTML = customRunHtml(await api.run(lang, ex.code, ex.stdin || ""));
    } catch (e) {
      toast(e.message, true);
    } finally {
      spinBtn(btn, false);
    }
  }));
  $$("[data-edit]").forEach((btn) => btn.addEventListener("click", () => {
    const ex = l.examples[+btn.dataset.edit];
    storage("cq-playground-load", { lang, code: ex.code, stdin: ex.stdin || "" });
    location.hash = "#/play";
  }));
  const mark = $("#mark-done");
  if (mark) mark.addEventListener("click", async () => {
    try {
      const r = await api.completeLesson(id);
      celebrate(r, { title: "Lesson complete!" });
      lessonView({ id });
    } catch (e) {
      toast(e.message, true);
    }
  });

  if (l.challenge) {
    const ed = createEditor($("#ch-editor"), {
      lang, value: l.challenge.draft ?? l.challenge.starter, fontSize: state.settings?.font_size,
      onChange: (code) => api.saveDraft(`lesson:${id}`, code).catch(() => {}),
    });
    state.cleanup = () => ed.flush();
    const go = async (mode, btn) => {
      spinBtn(btn, true);
      try {
        const res = await api.lessonChallenge(id, ed.getValue(), mode);
        $("#ch-result").innerHTML = resultHtml(res, { submit: mode === "submit" });
        $("#ch-result").scrollIntoView({ behavior: "smooth", block: "nearest" });
        if (res.reward) celebrate(res.reward, { title: "Challenge passed!" });
        if (res.solution) $("#ch-solution").innerHTML = solutionHtml({ [lang]: res.solution });
      } catch (e) {
        toast(e.message, true);
      } finally {
        spinBtn(btn, false);
      }
    };
    $("#ch-run").addEventListener("click", (e) => go("run", e.currentTarget));
    $("#ch-submit").addEventListener("click", (e) => go("submit", e.currentTarget));
  }
}

async function practiceView() {
  setTitle("Practice");
  setTab("practice");
  const d = await api.problems();
  const f = Object.assign({ lang: state.settings?.preferred_lang || "python", diff: "all", cat: "all", status: "all", q: "" },
    storage("cq-practice-filter") || {});
  view.innerHTML = `
    <div class="seg" id="lang-seg">
      <button data-l="python">🐍 Python</button><button data-l="cpp">⚡ C++</button>
    </div>
    <div class="chips mt" id="diff-chips">
      ${["all", ...d.difficulties].map((x) => `<button class="chip" data-d="${x}">${x === "all" ? "All levels" : DIFF_LABEL[x]}</button>`).join("")}
    </div>
    <div class="row mt">
      <select id="cat" class="grow" aria-label="Category"><option value="all">All categories</option>
        ${d.categories.map((c) => `<option value="${esc(c)}">${c === "Math & Data" ? "🧮 " : ""}${esc(c)}</option>`).join("")}</select>
      <select id="status" style="width:auto" aria-label="Status"><option value="all">All</option><option value="todo">Unsolved</option>
        <option value="solved">Solved</option></select>
    </div>
    <input type="search" id="q" class="mt" placeholder="Search problems…" value="${esc(f.q)}">
    <p class="small muted" id="count"></p>
    <div class="list" id="plist"></div>`;
  $("#cat").value = f.cat;
  $("#status").value = f.status;

  function render() {
    storage("cq-practice-filter", f);
    $$("#lang-seg button").forEach((b) => b.classList.toggle("on", b.dataset.l === f.lang));
    $$("#diff-chips .chip").forEach((b) => b.classList.toggle("on", b.dataset.d === f.diff));
    const q = f.q.trim().toLowerCase();
    const items = d.problems.filter((p) =>
      p.languages.includes(f.lang) &&
      (f.diff === "all" || p.difficulty === f.diff) &&
      (f.cat === "all" || p.category === f.cat) &&
      (f.status === "all" || (f.status === "solved") === p.solved.includes(f.lang)) &&
      (!q || p.title.toLowerCase().includes(q) || p.tags.some((t) => t.includes(q)) || p.category.toLowerCase().includes(q)));
    const solvedHere = items.filter((p) => p.solved.includes(f.lang)).length;
    $("#count").textContent = `${items.length} problems · ${solvedHere} solved in ${LANG_NAME[f.lang]}`;
    $("#plist").innerHTML = items.map((p) => {
      const done = p.solved.includes(f.lang);
      const cls = done ? "done" : p.attempted ? "tried" : "";
      return `<a class="list-item" href="#/problem/${p.id}?lang=${f.lang}">
        <div class="check ${cls}">${done ? "✓" : p.attempted ? "•" : ""}</div>
        <div class="grow"><b>${esc(p.title)}</b>
          <div class="row wrap small" style="gap:6px;margin-top:3px">${diffBadge(p.difficulty)}<span class="tag">${esc(p.category)}</span>
          ${p.solved.length && !done ? `<span class="tag">✓ ${p.solved.map((l) => LANG_NAME[l]).join(", ")}</span>` : ""}</div></div>
        <span class="muted small">+${p.xp}</span></a>`;
    }).join("") || `<div class="list-item muted">No problems match these filters.</div>`;
  }
  $$("#lang-seg button").forEach((b) => b.addEventListener("click", () => { f.lang = b.dataset.l; render(); }));
  $$("#diff-chips .chip").forEach((b) => b.addEventListener("click", () => { f.diff = b.dataset.d; render(); }));
  $("#cat").addEventListener("change", (e) => { f.cat = e.target.value; render(); });
  $("#status").addEventListener("change", (e) => { f.status = e.target.value; render(); });
  $("#q").addEventListener("input", (e) => { f.q = e.target.value; render(); });
  render();
}

async function problemView({ id }, query) {
  state.codingView = true;
  const p = await api.problem(id);
  setTitle(p.title, "#/practice");
  setTab("practice");
  let lang = query.get("lang") || state.settings?.preferred_lang || "python";
  if (!p.languages.includes(lang)) lang = p.languages[0];
  let tab = "desc";

  view.innerHTML = `
    <div class="seg" id="ptabs"><button data-tab="desc" class="on">📝 Problem</button><button data-tab="code">💻 Code</button></div>
    <section id="tab-desc" class="mt">
      <div class="row wrap small" style="gap:6px">${diffBadge(p.difficulty)}<span class="tag">${esc(p.category)}</span>
        ${p.tags.map((t) => `<span class="tag">#${esc(t)}</span>`).join("")}</div>
      <h2 style="margin:10px 0">${esc(p.title)} ${p.solved.length ? `<span style="color:var(--ok)">✓</span>` : ""}</h2>
      ${p.inspired_by ? `<p class="small muted">Inspired by ${esc(p.inspired_by)}</p>` : ""}
      <div class="card md">${markdown(p.statement)}
        <h3>Input</h3>${markdown(p.input_format)}<h3>Output</h3>${markdown(p.output_format)}</div>
      <div class="section-title">Examples</div>
      ${p.samples.map((s, i) => `<div class="card"><b class="small">Example ${i + 1}</b><div class="two-col">
        <div><div class="io-label">Input</div><div class="output">${esc(s.input)}</div></div>
        <div><div class="io-label">Output</div><div class="output">${esc(s.output)}</div></div></div></div>`).join("")}
      <p class="small muted">+ ${p.hidden_test_count} hidden tests · time limit ${p.time_limit}s per test
        ${p.checker === "float" ? "· decimals compared with 1e-6 tolerance" : ""}
        ${p.checker === "sympy" ? "· expressions compared symbolically" : ""}
        ${p.checker === "unordered" ? "· any line order accepted" : ""}</p>
      <div class="section-title">Hints</div>
      <div id="hints"></div>
      <div id="history"></div>
      <div id="solution">${solutionHtml(p.solution)}</div>
      <button class="btn primary block mt" id="to-code">Start coding ›</button>
    </section>
    <section id="tab-code" class="mt hidden">
      ${p.languages.length > 1 ? `<div class="seg" id="plang"><button data-l="python">🐍 Python</button><button data-l="cpp">⚡ C++</button></div>` :
        `<p class="small muted">${p.category === "Math & Data" ? "🧮 Python-only problem: NumPy & SymPy are available." : "Python only."}</p>`}
      <div class="mt" id="peditor"></div>
      <div class="toolbar">
        <button class="btn" id="run">▶ Run</button>
        <button class="btn" id="custom-toggle">⌨ Input</button>
        <button class="btn go" id="submit">🚀 Submit</button>
      </div>
      <div id="custom" class="hidden mt"><div class="io-label">Custom input</div>
        <textarea class="plain" id="custom-in">${esc(p.samples[0]?.input || "")}</textarea>
        <button class="btn small mt" id="custom-run">▶ Run with this input</button></div>
      <div class="row mt small muted"><button class="btn small ghost" id="reset">↺ Reset to starter</button>
        <span class="grow"></span><span id="xp-now"></span></div>
      <div id="presult" class="mt"></div>
    </section>`;

  const switchTab = (t) => {
    tab = t;
    $$("#ptabs button").forEach((b) => b.classList.toggle("on", b.dataset.tab === t));
    $("#tab-desc").classList.toggle("hidden", t !== "desc");
    $("#tab-code").classList.toggle("hidden", t !== "code");
    window.scrollTo(0, 0);
  };
  $$("#ptabs button").forEach((b) => b.addEventListener("click", () => switchTab(b.dataset.tab)));
  $("#to-code").addEventListener("click", () => switchTab("code"));

  // --- hints
  let hints = p.hints.slice();
  let xpNow = p.xp_now;
  function renderHints() {
    const left = p.hint_count - hints.length;
    $("#hints").innerHTML = hints.map((h, i) => `<div class="hint md"><b>Hint ${i + 1}:</b> ${markdown(h)}</div>`).join("") +
      (left > 0 ? `<button class="btn block" id="hint-btn">💡 Reveal hint ${hints.length + 1} of ${p.hint_count}
          <span class="muted small">(−15% XP)</span></button>`
        : `<p class="small muted">All hints revealed. You've got this! 💪</p>`);
    $("#xp-now").textContent = p.solved.includes(lang) ? "Solved ✓" : `Worth ${xpNow} XP`;
    const btn = $("#hint-btn");
    if (btn) btn.addEventListener("click", async () => {
      spinBtn(btn, true);
      try {
        const r = await api.hint(id);
        hints.push(r.hint);
        xpNow = r.xp_now;
        renderHints();
      } catch (e) {
        toast(e.message, true);
        spinBtn(btn, false);
      }
    });
  }
  function renderHistory(items) {
    if (!items.length) return ($("#history").innerHTML = "");
    $("#history").innerHTML = `<div class="section-title">Your attempts</div><div class="list">${items.map((h) => `
      <div class="list-item small"><span>${h.verdict === "ok" ? "✅" : "❌"}</span><span class="grow">${VERDICT_TEXT[h.verdict] || h.verdict}
        · ${h.passed}/${h.total}</span><span class="muted">${LANG_NAME[h.lang]}</span></div>`).join("")}</div>`;
  }
  renderHints();
  renderHistory(p.history);

  // --- editor
  const ed = createEditor($("#peditor"), {
    lang, value: p.drafts[lang] ?? p.starter[lang], fontSize: state.settings?.font_size,
    onChange: (code) => api.saveDraft(`problem:${id}:${lang}`, code).catch(() => {}),
  });
  state.cleanup = () => ed.flush();
  const drafts = { ...p.drafts };
  function setLang(l) {
    if (l === lang) return;
    ed.flush();
    drafts[lang] = ed.getValue();
    lang = l;
    ed.setLang(l);
    ed.setValue(drafts[l] ?? p.starter[l]);
    $$("#plang button").forEach((b) => b.classList.toggle("on", b.dataset.l === l));
    renderHints();
    if (state.settings && state.settings.preferred_lang !== l) {
      state.settings.preferred_lang = l;
      api.saveSettings({ preferred_lang: l }).catch(() => {});
    }
  }
  $$("#plang button").forEach((b) => {
    b.classList.toggle("on", b.dataset.l === lang);
    b.addEventListener("click", () => setLang(b.dataset.l));
  });
  $("#reset").addEventListener("click", async () => {
    if (await confirmDialog("Replace your code with the starter template?", "Reset")) ed.setValue(p.starter[lang]);
  });
  $("#custom-toggle").addEventListener("click", () => $("#custom").classList.toggle("hidden"));

  const showResult = (html) => {
    $("#presult").innerHTML = html;
    $("#presult").scrollIntoView({ behavior: "smooth", block: "start" });
  };
  $("#run").addEventListener("click", async (e) => {
    const btn = e.currentTarget;
    spinBtn(btn, true);
    try {
      showResult(resultHtml(await api.runProblem(id, lang, ed.getValue()), { submit: false }));
    } catch (err) {
      toast(err.message, true);
    } finally {
      spinBtn(btn, false);
    }
  });
  $("#custom-run").addEventListener("click", async (e) => {
    const btn = e.currentTarget;
    spinBtn(btn, true);
    try {
      showResult(customRunHtml(await api.runProblem(id, lang, ed.getValue(), $("#custom-in").value)));
    } catch (err) {
      toast(err.message, true);
    } finally {
      spinBtn(btn, false);
    }
  });
  $("#submit").addEventListener("click", async (e) => {
    const btn = e.currentTarget;
    spinBtn(btn, true);
    try {
      const res = await api.submit(id, lang, ed.getValue());
      showResult(resultHtml(res, { submit: true }));
      if (res.verdict === "ok") {
        if (!p.solved.includes(lang)) p.solved.push(lang);
        renderHints();
        if (res.reward?.first_solve) {
          celebrate(res.reward, { title: "Accepted!", subtitle: `${p.title} · ${LANG_NAME[lang]}` });
        } else {
          updateTopbar(res.reward?.level, res.reward?.streak);
          toast("Accepted again ✓ (XP is only awarded on the first solve)");
        }
        $("#solution").innerHTML = solutionHtml(res.solution);
      }
      api.problem(id).then((fresh) => renderHistory(fresh.history)).catch(() => {});
    } catch (err) {
      toast(err.message, true);
    } finally {
      spinBtn(btn, false);
    }
  });
  if (query.get("tab") === "code") switchTab("code");
}

const PLAY_TEMPLATES = {
  python: `# Playground: experiment freely!\nimport math\n\nname = input() or "world"\nprint(f"Hello, {name}!")\nprint("pi is about", round(math.pi, 4))\n`,
  cpp: `#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string name;\n    getline(cin, name);\n    if (name.empty()) name = "world";\n    cout << "Hello, " << name << "!\\n";\n    return 0;\n}\n`,
};

async function playView() {
  state.codingView = true;
  setTitle("Playground");
  setTab("play");
  const loaded = storage("cq-playground-load");
  if (loaded) storage("cq-playground-load", null);
  let lang = loaded?.lang || state.settings?.preferred_lang || "python";
  const draft = loaded ? null : (await api.get(`/api/drafts?key=playground:${lang}`)).code;
  view.innerHTML = `
    <div class="seg" id="play-lang"><button data-l="python">🐍 Python</button><button data-l="cpp">⚡ C++</button></div>
    <div class="mt" id="play-editor"></div>
    <div class="io-label">Input (stdin)</div>
    <textarea class="plain" id="play-in" placeholder="Text your program reads with input() / cin">${esc(loaded?.stdin || "")}</textarea>
    <div class="toolbar"><button class="btn go" id="play-run">▶ Run</button>
      <button class="btn ghost" id="play-reset">↺ Template</button></div>
    <div id="play-out" class="mt"></div>
    <p class="small muted mt">Python has NumPy & SymPy available when installed. C++ is compiled with -std=c++17 -O2.</p>`;
  const ed = createEditor($("#play-editor"), {
    lang, value: loaded?.code ?? draft ?? PLAY_TEMPLATES[lang], fontSize: state.settings?.font_size,
    onChange: (code) => api.saveDraft(`playground:${lang}`, code).catch(() => {}),
  });
  state.cleanup = () => ed.flush();
  const mark = () => $$("#play-lang button").forEach((b) => b.classList.toggle("on", b.dataset.l === lang));
  mark();
  $$("#play-lang button").forEach((b) => b.addEventListener("click", async () => {
    if (b.dataset.l === lang) return;
    ed.flush();
    lang = b.dataset.l;
    mark();
    ed.setLang(lang);
    const d = await api.get(`/api/drafts?key=playground:${lang}`).catch(() => ({}));
    ed.setValue(d.code ?? PLAY_TEMPLATES[lang]);
  }));
  $("#play-reset").addEventListener("click", () => ed.setValue(PLAY_TEMPLATES[lang]));
  $("#play-run").addEventListener("click", async (e) => {
    const btn = e.currentTarget;
    spinBtn(btn, true);
    try {
      $("#play-out").innerHTML = customRunHtml(await api.run(lang, ed.getValue(), $("#play-in").value));
      $("#play-out").scrollIntoView({ behavior: "smooth", block: "nearest" });
    } catch (err) {
      toast(err.message, true);
    } finally {
      spinBtn(btn, false);
    }
  });
}

async function profileView() {
  setTitle("Profile");
  setTab("profile");
  const [d, health] = await Promise.all([api.profile(), state.health ? state.health : api.health()]);
  state.health = health;
  const s = state.settings || (await api.settings());
  updateTopbar(d.level, d.streak.current);
  const lv = d.level;
  const maxMin = Math.max(d.time.goal_minutes, ...d.time.days.map((x) => x.minutes), 1);
  const bars = d.time.days.map((x) =>
    `<div class="bar ${x.minutes >= d.time.goal_minutes ? "goal" : ""}" title="${x.date}: ${x.minutes} min">
      <i style="height:${Math.round((x.minutes / maxMin) * 100)}%"></i></div>`).join("");
  const labels = d.time.days.map((x) =>
    `<span>${new Date(x.date + "T12:00:00").toLocaleDateString(undefined, { weekday: "narrow" })}</span>`).join("");
  const diffs = ["beginner", "easy", "medium", "hard", "expert"];
  const maxDiff = Math.max(1, ...diffs.map((k) => d.problems.by_difficulty[k] || 0));
  const rate = d.problems.attempts ? Math.round(((d.problems.attempts - d.problems.failed_attempts) / d.problems.attempts) * 100) : 0;
  const earned = d.badges.filter((b) => b.earned_at).length;
  view.innerHTML = `
    <div class="card hero"><div class="row"><div class="level-badge">${lv.level}</div><div class="grow">
      <div style="font-weight:800;font-size:18px">${esc(lv.title)}</div>
      <div class="muted small">${lv.xp} XP total · next level at ${lv.level_end}</div>
      <div class="progress mt"><i style="width:${Math.round(lv.progress * 100)}%"></i></div></div></div></div>
    <div class="stat-grid">
      <div class="stat"><div class="v">🔥 ${d.streak.current}</div><div class="k">Streak (best ${d.streak.best})</div></div>
      <div class="stat"><div class="v">${d.problems.solved}</div><div class="k">Solved</div></div>
      <div class="stat"><div class="v">${d.lessons.done}</div><div class="k">Lessons</div></div>
      <div class="stat"><div class="v">${Math.round(d.time.today_minutes)}m</div><div class="k">Today</div></div>
      <div class="stat"><div class="v">${(d.time.total_minutes / 60).toFixed(1)}h</div><div class="k">Total time</div></div>
      <div class="stat"><div class="v">${rate}%</div><div class="k">Accept rate</div></div>
    </div>
    <div class="section-title">Coding minutes · last 14 days</div>
    <div class="card"><div class="bars">${bars}
      <div class="goal-line" style="bottom:${(d.time.goal_minutes / maxMin) * 100}%"></div></div>
      <div class="bar-labels">${labels}</div>
      <p class="small muted">Dashed line: daily goal (${d.time.goal_minutes} min). Only active time in lessons, problems and the playground counts.</p></div>
    <div class="section-title">Problems</div>
    <div class="card">
      ${diffs.map((k) => `<div class="hbar"><span>${diffBadge(k)}</span>
        <div class="progress"><i style="width:${((d.problems.by_difficulty[k] || 0) / maxDiff) * 100}%"></i></div>
        <b>${d.problems.by_difficulty[k] || 0}</b></div>`).join("")}
      <p class="small muted">${d.problems.attempts} submissions · ${d.problems.failed_attempts} failed ·
        🐍 ${d.problems.by_language.python || 0} · ⚡ ${d.problems.by_language.cpp || 0} solved by language</p>
    </div>
    <div class="section-title">Badges · ${earned}/${d.badges.length}</div>
    <div class="badges">${d.badges.map((b) => `<div class="badge ${b.earned_at ? "" : "locked"}" title="${esc(b.description)}">
      <div class="bi">${b.icon}</div><div class="bn">${esc(b.name)}</div><div class="bd">${esc(b.description)}</div></div>`).join("")}</div>
    ${d.recent.length ? `<div class="section-title">Recent submissions</div><div class="list">${d.recent.map((r) => `
      <a class="list-item small" href="#/problem/${r.problem_id}?lang=${r.lang}"><span>${r.verdict === "ok" ? "✅" : "❌"}</span>
        <span class="grow"><b>${esc(r.title)}</b> <span class="muted">${VERDICT_TEXT[r.verdict] || r.verdict} ${r.passed}/${r.total}</span></span>
        <span class="muted">${LANG_NAME[r.lang]} · ${esc(r.when)}</span></a>`).join("")}</div>` : ""}
    <div class="section-title">Settings</div>
    <div class="card">
      <label class="small muted">Daily goal (minutes)</label>
      <input type="number" id="set-goal" min="1" max="600" value="${s.daily_goal}">
      <label class="small muted mt" style="display:block">Code font size</label>
      <input type="number" id="set-font" min="10" max="24" value="${s.font_size}">
      <label class="small muted mt" style="display:block">Termux judge URL (for C++ inside the APK)</label>
      <input type="url" id="set-judge" placeholder="http://127.0.0.1:8765" value="${esc(s.remote_judge)}">
      <button class="btn primary block mt" id="save-settings">Save settings</button>
      <button class="btn block mt" id="export">⬇ Export progress (JSON)</button>
    </div>
    <div class="section-title">System</div>
    <div class="card small">
      <div>Version ${esc(health.version)} · ${health.android_app ? "Android app" : health.termux ? "Termux" : "Desktop"}</div>
      <div>Python runner: ${esc(health.python.mode)} · NumPy ${health.libraries.numpy ? "✓" : "✗"} · SymPy ${health.libraries.sympy ? "✓" : "✗"}</div>
      <div>C++: ${health.cpp.local ? esc(health.cpp.compiler) : health.cpp.remote ? "via Termux judge " + esc(health.cpp.remote) : "unavailable (install clang in Termux)"}</div>
      <div>Library: ${health.counts.problems} problems · ${health.counts.lessons_python} Python + ${health.counts.lessons_cpp} C++ lessons</div>
    </div>`;
  $("#export").addEventListener("click", async () => {
    if (!health.android_app) {
      location.href = "/api/export";
      return;
    }
    // Downloads don't work in the APK's WebView: show the JSON to copy instead.
    const data = JSON.stringify(await api.get("/api/export"));
    const m = modal(`<h3>Your progress</h3><textarea class="plain" readonly style="min-height:200px">${esc(data)}</textarea>
      <div class="row mt"><button class="btn grow" data-close>Close</button><button class="btn primary grow" id="copy-export">Copy</button></div>`);
    m.root.querySelector("#copy-export").addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(data);
        toast("Copied ✓");
      } catch (e) {
        m.root.querySelector("textarea").select();
        toast("Select all & copy manually", true);
      }
    });
  });
  $("#save-settings").addEventListener("click", async () => {
    try {
      state.settings = await api.saveSettings({
        daily_goal: +$("#set-goal").value, font_size: +$("#set-font").value, remote_judge: $("#set-judge").value,
      });
      state.health = null;
      toast("Settings saved ✓");
      profileView();
    } catch (e) {
      toast(e.message, true);
    }
  });
}

// ---------------------------------------------------------------- router
const ROUTES = [
  [/^\/?$/, homeView],
  [/^\/learn\/(?<track>\w+)$/, learnView],
  [/^\/lesson\/(?<id>[\w-]+)$/, lessonView],
  [/^\/practice$/, practiceView],
  [/^\/problem\/(?<id>[\w-]+)$/, problemView],
  [/^\/play$/, playView],
  [/^\/profile$/, profileView],
];

async function route() {
  if (state.cleanup) {
    try { state.cleanup(); } catch (e) { /* ignore */ }
    state.cleanup = null;
  }
  flushTracker();
  document.querySelectorAll(".confetti").forEach((c) => c.remove());
  document.getElementById("modal-root").innerHTML = "";
  state.codingView = false;
  document.body.classList.remove("editing");
  const raw = location.hash.replace(/^#/, "") || "/";
  const [path, qs] = raw.split("?");
  const query = new URLSearchParams(qs || "");
  const match = ROUTES.map(([re, fn]) => [path.match(re), fn]).find(([m]) => m);
  window.scrollTo(0, 0);
  if (!match) {
    location.hash = "#/";
    return;
  }
  loading();
  try {
    await match[1](match[0].groups || {}, query);
  } catch (e) {
    console.error(e);
    errorView(e);
  }
  view.focus({ preventScroll: true });
}

async function boot() {
  try {
    state.settings = await api.settings();
  } catch (e) {
    state.settings = null;
  }
  addEventListener("hashchange", route);
  route();
}

boot();
