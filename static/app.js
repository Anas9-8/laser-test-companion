// Alle reaktiven Daten der Single-Page-App
// Alpine.js liest diese Funktion über x-data="appData()" ein
function appData() {
  return {
    // aktive Ansicht (Routing über x-show)
    view: 'overview',

    // gemeinsame State-Container die alle Seiten brauchen
    stats: null,
    testCases: [],
    bugs: [],
    requirements: [],
    sprint: null,
    trace: [],
    trend: [],

    // UI-State pro Seite
    filterModule: '',
    filterStatus: '',
    selectedTc: null,
    showNewTcModal: false,
    newTc: { title: '', module: 'Surgeon UI', requirement_id: 'REQ-SUI-12', steps_raw: '' },

    // Squish-Simulator State
    squishSelected: 'TC-1042',
    autMode: 'attachable',
    running: false,
    runLines: [],
    runResult: null,
    runDuration: 0,
    runReport: null,
    runScreenshot: null,
    runAutoBug: null,

    // Bug-Tracking State
    selectedBug: null,
    newBug: {
      title: '', module: 'Surgeon UI', severity: 'Major',
      linked_test: '', linked_requirement: '',
      description: '', steps_to_reproduce: '', expected: '', actual: ''
    },

    // Toast-Meldungen unten rechts
    toast: '',

    // statische Daten für Diagramme — bewusst hier statt aus dem Backend,
    // weil das nur Beschriftungen sind die sich nie ändern
    bugColumns: [
      { key: 'OPEN',        label: '📥 OPEN' },
      { key: 'IN_PROGRESS', label: '🔄 IN PROGRESS' },
      { key: 'IN_REVIEW',   label: '🧪 IN REVIEW' },
      { key: 'IN_TEST',     label: '🚀 IN TEST' },
      { key: 'CLOSED',      label: '✅ CLOSED' },
    ],
    storyColumns: [
      { key: 'TODO',        label: 'TO DO',       bg: '#fff8e1', fg: '#7c5300' },
      { key: 'IN_PROGRESS', label: 'IN PROGRESS', bg: '#e3f2fd', fg: '#0d47a1' },
      { key: 'DONE',        label: 'DONE',        bg: '#e8f5e9', fg: '#1b5e20' },
    ],
    lifecycleSteps: [
      { label: 'Anforderung', color: '#1565C0', desc: 'REQ-ID lesen' },
      { label: 'Design',      color: '#1976D2', desc: 'Schritte planen' },
      { label: 'Recording',   color: '#6A1B9A', desc: 'Squish-IDE aufnehmen' },
      { label: 'Skript',      color: '#7B1FA2', desc: 'Python verfeinern' },
      { label: 'SVN-Commit',  color: '#37474F', desc: 'in Trunk pushen' },
      { label: 'CI-Lauf',     color: '#2E7D32', desc: 'Jenkins triggert' },
      { label: 'Review',      color: '#E65100', desc: 'Pair-Review' },
    ],
    bugLifecycle: [
      { label: 'Test fehlgeschlagen', color: '#C62828', desc: 'Squish meldet FAIL' },
      { label: 'In Jira erfasst',     color: '#E65100', desc: 'Mit Screenshot + Logs' },
      { label: 'Triage',              color: '#F57F17', desc: 'Schweregrad im Daily' },
      { label: 'Fix im Code',         color: '#37474F', desc: 'SVN-Commit Entwickler' },
      { label: 'Re-Test Squish',      color: '#1565C0', desc: 'Tester verifiziert' },
      { label: 'Closed / Reopen',     color: '#2E7D32', desc: 'Bug schließen' },
    ],
    iecNodes: [
      'Software Development Planning',
      'Software Requirements Analysis',
      'Software Architectural Design',
      'Software Detailed Design',
      'Software Unit Implementation',
      'Software Integration Testing',
      'Software System Testing',
      'Software Release',
    ],

    // Beim Start ziehen wir alle Daten aus dem Backend
    async init() {
      await Promise.all([
        this.refreshStats(),
        this.refreshTestCases(),
        this.refreshBugs(),
        this.refreshRequirements(),
        this.refreshSprint(),
        this.refreshTrace(),
        this.refreshTrend(),
      ]);
    },

    // einfache Fetch-Wrapper — übersichtlicher als überall fetch zu schreiben
    async refreshStats()        { this.stats        = await fetch('/api/stats').then(r=>r.json()); },
    async refreshTestCases()    { this.testCases    = await fetch('/api/test-cases').then(r=>r.json()); },
    async refreshBugs()         { this.bugs         = await fetch('/api/bugs').then(r=>r.json()); },
    async refreshRequirements() { this.requirements = await fetch('/api/requirements').then(r=>r.json()); },
    async refreshSprint()       { this.sprint       = await fetch('/api/sprint').then(r=>r.json()); },
    async refreshTrace()        { this.trace        = await fetch('/api/traceability').then(r=>r.json()); },
    async refreshTrend()        { this.trend        = await fetch('/api/runs/trend').then(r=>r.json()); },

    // gefilterte Liste der Testfälle für die Karten-Ansicht
    get filteredTestCases() {
      return this.testCases.filter(tc =>
        (!this.filterModule || tc.module === this.filterModule) &&
        (!this.filterStatus || tc.status === this.filterStatus)
      );
    },

    // Farbcode pro Testfall-Status — wird auch für Border und Badge benutzt
    tcColor(s) {
      return ({
        implementiert: '#2E7D32',
        in_arbeit:     '#F57F17',
        zu_reviewen:   '#1565C0',
        failed:        '#C62828',
      })[s] || '#94a3b8';
    },
    tcStatusLabel(s) {
      return ({
        implementiert: 'Implementiert',
        in_arbeit:     'In Arbeit',
        zu_reviewen:   'Zu reviewen',
        failed:        'Failed',
      })[s] || s;
    },

    // Testfall anlegen über das Formular im Modal
    async createTestCase() {
      const steps = this.newTc.steps_raw.split('\n').map(s=>s.trim()).filter(Boolean);
      const res = await fetch('/api/test-cases', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: this.newTc.title,
          module: this.newTc.module,
          requirement_id: this.newTc.requirement_id,
          steps: steps,
        }),
      });
      if (res.ok) {
        const created = await res.json();
        this.showToast(`Testfall ${created.id} angelegt.`);
        this.showNewTcModal = false;
        this.newTc = { title:'', module:'Surgeon UI', requirement_id:'REQ-SUI-12', steps_raw:'' };
        await this.refreshTestCases();
      }
    },

    // Squish-Lauf simulieren — wir lassen die Zeilen einzeln im 350-ms-Takt einlaufen
    async runSquish() {
      this.runLines = [];
      this.runResult = null;
      this.runReport = null;
      this.runScreenshot = null;
      this.runAutoBug = null;
      this.running = true;

      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ test_case_id: this.squishSelected, aut_mode: this.autMode }),
      });
      const data = await res.json();

      // Schritte zeichnen — kleine Pause zwischen jeder Zeile,
      // damit es aussieht als würde Squish gerade live laufen
      for (let i = 0; i < data.steps.length; i++) {
        await new Promise(r => setTimeout(r, 350));
        this.runLines.push({ id: i, text: data.steps[i].text, ok: data.steps[i].ok });
        await new Promise(r => setTimeout(r, 50));
        if (this.$refs.console) {
          this.$refs.console.scrollTop = this.$refs.console.scrollHeight;
        }
      }

      // am Ende das Gesamtergebnis anzeigen
      await new Promise(r => setTimeout(r, 250));
      this.runResult = data.result;
      this.runDuration = data.duration_seconds;
      this.runReport = data.report_path;
      this.runScreenshot = data.screenshot;
      this.runAutoBug = data.auto_bug;
      this.running = false;
    },

    // Pass-Rate für die Trend-Balken in Prozent
    passRate(r) { return Math.round(100 * r.passed / r.total); },

    // Bug-Detail-Status-Wechsel
    async moveBug(id, status) {
      await fetch(`/api/bugs/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      });
      await this.refreshBugs();
      this.selectedBug = null;
      this.showToast(`Bug ${id} verschoben nach ${status.replace('_',' ')}.`);
    },

    // Schweregrad-Farbe für Karten und Modals
    sevColor(s) {
      return ({
        Critical: '#C62828', Blocker: '#4a148c',
        Major:    '#F57F17', Minor: '#1976D2', Trivial: '#94a3b8',
      })[s] || '#94a3b8';
    },

    // Donut-Chart Gradient aus den offenen Bugs nach Schweregrad bauen
    get donutGradient() {
      const open = this.bugs.filter(b => b.status !== 'CLOSED');
      const groups = { Critical: 0, Major: 0, Minor: 0, Other: 0 };
      open.forEach(b => {
        if (groups[b.severity] !== undefined) groups[b.severity] += 1;
        else groups.Other += 1;
      });
      const total = open.length || 1;
      let acc = 0;
      const slice = (count, color) => {
        const start = (acc / total) * 360;
        acc += count;
        const end = (acc / total) * 360;
        return `${color} ${start}deg ${end}deg`;
      };
      return `conic-gradient(${slice(groups.Critical, '#C62828')}, ${slice(groups.Major, '#F57F17')}, ${slice(groups.Minor, '#1976D2')}, ${slice(groups.Other, '#94a3b8')})`;
    },

    // Bug aus Formular speichern
    async submitBug() {
      const res = await fetch('/api/bugs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.newBug),
      });
      if (res.ok) {
        const created = await res.json();
        this.showToast(`Bug ${created.id} wurde im Jira-System angelegt.`);
        this.newBug = { title:'', module:'Surgeon UI', severity:'Major',
          linked_test:'', linked_requirement:'', description:'', steps_to_reproduce:'', expected:'', actual:'' };
        await this.refreshBugs();
        await this.refreshStats();
      }
    },

    // Story im Sprint-Backlog verschieben
    async moveStory(id, status) {
      await fetch(`/api/sprint/story/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      });
      await this.refreshSprint();
      await this.refreshStats();
      this.showToast(`Story ${id} verschoben.`);
    },

    // Status-Hilfsfunktionen für die Traceability-Matrix
    statusClass(s) {
      if (s === 'PASS') return 'status-pass';
      if (s === 'FAIL') return 'status-fail';
      if (s === 'WIP')  return 'status-wip';
      return '';
    },
    statusLabel(s) {
      return ({ PASS: '✅ PASS', FAIL: '❌ FAIL', WIP: '⏳ WIP' })[s] || s;
    },

    // Position der 8 IEC-Knoten als Kreis berechnen
    iecPosition(i) {
      const angle = (i / 8) * 2 * Math.PI - Math.PI / 2;
      const r = 200;
      const cx = 240 - 65;
      const cy = 240 - 26;
      const x = cx + r * Math.cos(angle);
      const y = cy + r * Math.sin(angle);
      return `left: ${x}px; top: ${y}px;`;
    },

    // Toast-Meldung kurz anzeigen und nach 3 s wegblenden
    showToast(msg) {
      this.toast = msg;
      setTimeout(() => { this.toast = ''; }, 3000);
    },
  };
}
