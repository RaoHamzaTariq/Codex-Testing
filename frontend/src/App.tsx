import {
  Activity,
  Bell,
  Bolt,
  Calendar,
  CheckCircle2,
  ChevronDown,
  Clock,
  FileText,
  Gauge,
  Inbox,
  LayoutDashboard,
  PauseCircle,
  Settings,
  Shield,
  Sparkles,
  User,
} from "lucide-react";
import { LineChart, Line, ResponsiveContainer } from "recharts";
import { useEffect } from "react";
import { Badge } from "./components/ui/badge";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { useDashboardStore } from "./store";

const navigation = [
  { label: "Overview", icon: LayoutDashboard },
  { label: "Inbox", icon: Inbox },
  { label: "Action", icon: Bolt },
  { label: "Done", icon: CheckCircle2 },
  { label: "Pending", icon: Clock },
  { label: "Analytics", icon: Gauge },
  { label: "Logs", icon: FileText },
  { label: "Settings", icon: Settings },
];

const quickActions = [
  { label: "+ Task", icon: Sparkles },
  { label: "Pause", icon: PauseCircle },
  { label: "Sync", icon: Activity },
];

const statusMap = {
  healthy: "bg-success",
  warning: "bg-warning",
  error: "bg-danger",
} as const;

export default function App() {
  const store = useDashboardStore();

  useEffect(() => {
    const interval = setInterval(() => store.tick(), 6000);
    return () => clearInterval(interval);
  }, [store]);

  return (
    <div className="min-h-screen bg-background text-white">
      <header className="flex items-center justify-between border-b border-white/10 px-6 py-4">
        <div className="flex items-center gap-3">
          <span className={`h-3 w-3 rounded-full ${statusMap[store.status]}`} />
          <div>
            <p className="text-sm font-semibold">AI Employee Status</p>
            <p className="text-xs text-white/60">Last update: {store.lastUpdated}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="ghost" className="flex items-center gap-2">
            <Bell className="h-4 w-4" />
            Notifications
          </Button>
          <Button variant="ghost" className="flex items-center gap-2">
            <Settings className="h-4 w-4" />
            Settings
          </Button>
          <Button variant="secondary" className="flex items-center gap-2">
            <User className="h-4 w-4" />
            Admin
            <ChevronDown className="h-3 w-3" />
          </Button>
        </div>
      </header>

      <div className="grid grid-cols-[260px_1fr] gap-6 p-6">
        <aside className="space-y-6">
          <nav className="rounded-xl border border-white/10 bg-card/60 p-4">
            <p className="mb-4 text-xs font-semibold uppercase text-white/40">Navigation</p>
            <div className="space-y-2">
              {navigation.map((item) => (
                <button
                  key={item.label}
                  className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-white/70 hover:bg-white/10 hover:text-white"
                >
                  <item.icon className="h-4 w-4" />
                  {item.label}
                </button>
              ))}
            </div>
          </nav>

          <div className="rounded-xl border border-white/10 bg-card/60 p-4">
            <p className="mb-4 text-xs font-semibold uppercase text-white/40">Quick Actions</p>
            <div className="space-y-3">
              {quickActions.map((action) => (
                <Button key={action.label} variant="secondary" className="w-full justify-start gap-2">
                  <action.icon className="h-4 w-4" />
                  {action.label}
                </Button>
              ))}
            </div>
          </div>
        </aside>

        <main className="space-y-6">
          <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>System Health</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <p className="text-2xl font-semibold">3 Watchers</p>
                  <Badge variant="success">Healthy</Badge>
                </div>
                <p className="text-xs text-white/60">Last check 30s ago</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Inbox Status</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-semibold">5 items</p>
                <p className="text-xs text-white/60">2 WhatsApp urgent · 1 file drop</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Pending Approvals</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <p className="text-2xl font-semibold">{store.approvals.length}</p>
                  <Badge variant="warning">Needs attention</Badge>
                </div>
                <p className="text-xs text-white/60">Payments and new contacts</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Today’s Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-semibold">{store.completedToday} tasks</p>
                <p className="text-xs text-white/60">{store.inProgress} in progress</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Weekly Revenue</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-semibold">$2,450</p>
                <div className="h-16">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={store.weeklyRevenue.map((value, index) => ({ day: index, value }))}>
                      <Line type="monotone" dataKey="value" stroke="#4f46e5" strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Active Projects</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-semibold">Project Alpha</p>
                <p className="text-xs text-white/60">Due Jan 15 · {store.projectProgress}% complete</p>
                <div className="mt-2 h-2 w-full rounded-full bg-white/10">
                  <div className="h-2 rounded-full bg-accent" style={{ width: `${store.projectProgress}%` }} />
                </div>
              </CardContent>
            </Card>
          </section>

          <section className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Inbox</CardTitle>
                  <div className="flex items-center gap-2 text-xs text-white/60">
                    <span>Filter: All</span>
                    <ChevronDown className="h-3 w-3" />
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {store.inbox.map((item) => (
                    <div
                      key={item.id}
                      className="rounded-lg border border-white/10 bg-white/5 p-3"
                    >
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-semibold">{item.title}</p>
                        <Badge variant={item.priority === "high" ? "danger" : "default"}>
                          {item.priority === "high" ? "High" : "Normal"}
                        </Badge>
                      </div>
                      <p className="text-xs text-white/60">{item.preview}</p>
                      <div className="mt-3 flex items-center gap-2">
                        <Button variant="secondary">View</Button>
                        <Button variant="primary">Let AI Handle</Button>
                        <Button variant="ghost">Mark Done</Button>
                        <span className="ml-auto text-xs text-white/40">{item.time}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Pending Approvals</CardTitle>
                  <Badge variant="danger">{store.approvals.length} urgent</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {store.approvals.map((approval) => (
                    <div
                      key={approval.id}
                      className="rounded-lg border border-white/10 bg-white/5 p-3"
                    >
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-semibold">{approval.title}</p>
                        <span className="text-xs text-white/50">{approval.expiresIn}</span>
                      </div>
                      <p className="text-xs text-white/70">{approval.detail}</p>
                      <p className="mt-2 text-xs text-white/50">AI reasoning: {approval.reasoning}</p>
                      <div className="mt-3 flex gap-2">
                        <Button variant="danger">Reject</Button>
                        <Button variant="secondary">Edit</Button>
                        <Button variant="primary">Approve</Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </section>

          <section className="grid gap-6 lg:grid-cols-[1fr_1fr]">
            <Card>
              <CardHeader>
                <CardTitle>CEO Briefing</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 text-xs text-white/70">
                  <p className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-accent" />
                    Weekly briefing generated today at 7:00 AM.
                  </p>
                  <p>
                    Revenue trend is on track. One bottleneck detected in the Client B proposal. Suggested
                    optimization: review unused subscriptions.
                  </p>
                  <Button variant="primary" className="w-full">
                    View Briefing
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Activity Log</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-xs text-white/70">
                  <div className="flex items-center justify-between">
                    <span>10:45 AM · email_send · client@a.com</span>
                    <Badge variant="success">Success</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>10:30 AM · plan_created · EMAIL_xxx</span>
                    <Badge variant="success">Success</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>10:15 AM · approval · PAYMENT_xxx</span>
                    <Badge variant="default">Approved</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>09:00 AM · watcher_trig · gmail_watcher</span>
                    <Badge variant="warning">Info</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          <section className="grid gap-6 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>Connection Status</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2 text-sm">
                  <span className="h-2 w-2 rounded-full bg-success" />
                  Connected · synced 2s ago
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Security</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2 text-sm">
                  <Shield className="h-4 w-4 text-accent" />
                  HITL approval required for payments
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Quick Command</CardTitle>
              </CardHeader>
              <CardContent>
                <Button variant="secondary" className="w-full">
                  Pause AI Operations
                </Button>
              </CardContent>
            </Card>
          </section>
        </main>
      </div>
    </div>
  );
}
