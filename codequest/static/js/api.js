// Thin JSON client for the CodeQuest server.

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function request(method, path, body) {
  const opts = {
    method,
    headers: { "X-TZ-Offset": String(new Date().getTimezoneOffset()) },
  };
  if (body !== undefined) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  }
  let res;
  try {
    res = await fetch(path, opts);
  } catch (e) {
    throw new ApiError("Can't reach the CodeQuest server. Is it running?", 0);
  }
  let data = null;
  try {
    data = await res.json();
  } catch (e) {
    /* non-JSON error */
  }
  if (!res.ok) throw new ApiError((data && data.error) || `HTTP ${res.status}`, res.status);
  return data;
}

export const api = {
  get: (p) => request("GET", p),
  post: (p, body = {}) => request("POST", p, body),
  health: () => request("GET", "/api/health"),
  home: () => request("GET", "/api/home"),
  lessons: (track) => request("GET", `/api/lessons?track=${encodeURIComponent(track)}`),
  lesson: (id) => request("GET", `/api/lessons/${id}`),
  completeLesson: (id) => request("POST", `/api/lessons/${id}/complete`, {}),
  lessonChallenge: (id, code, mode) => request("POST", `/api/lessons/${id}/challenge`, { code, mode }),
  problems: () => request("GET", "/api/problems"),
  problem: (id) => request("GET", `/api/problems/${id}`),
  hint: (id) => request("POST", `/api/problems/${id}/hint`, {}),
  runProblem: (id, lang, code, stdin) =>
    request("POST", `/api/problems/${id}/run`, stdin == null ? { lang, code } : { lang, code, stdin }),
  submit: (id, lang, code) => request("POST", `/api/problems/${id}/submit`, { lang, code }),
  run: (lang, code, stdin) => request("POST", "/api/run", { lang, code, stdin }),
  profile: () => request("GET", "/api/profile"),
  settings: () => request("GET", "/api/settings"),
  saveSettings: (s) => request("POST", "/api/settings", s),
  saveDraft: (key, code) => request("POST", "/api/drafts", { key, code }),
  heartbeat: (seconds) => request("POST", "/api/heartbeat", { seconds }),
};
