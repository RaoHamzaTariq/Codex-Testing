import { create } from "zustand";

export type StatusLevel = "healthy" | "warning" | "error";

export interface InboxItem {
  id: string;
  type: "email" | "whatsapp" | "file";
  title: string;
  preview: string;
  time: string;
  priority: "high" | "normal";
}

export interface ApprovalItem {
  id: string;
  type: "payment" | "email";
  title: string;
  detail: string;
  reasoning: string;
  expiresIn: string;
}

interface DashboardState {
  lastUpdated: string;
  status: StatusLevel;
  inbox: InboxItem[];
  approvals: ApprovalItem[];
  completedToday: number;
  inProgress: number;
  weeklyRevenue: number[];
  projectProgress: number;
  tick: () => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  lastUpdated: "2s ago",
  status: "healthy",
  inbox: [
    {
      id: "email-1",
      type: "email",
      title: "Client A - Invoice Request",
      preview: "Hey, can you send me the January invoice...",
      time: "2 min ago",
      priority: "high",
    },
    {
      id: "whatsapp-1",
      type: "whatsapp",
      title: "Supplier B - Urgent Payment",
      preview: "ASAP: Need payment confirmation for...",
      time: "15 min ago",
      priority: "high",
    },
    {
      id: "file-1",
      type: "file",
      title: "contract_draft.pdf dropped",
      preview: "New file received from shared folder.",
      time: "1 hour ago",
      priority: "normal",
    },
  ],
  approvals: [
    {
      id: "approval-1",
      type: "payment",
      title: "Payment request",
      detail: "Amount: $500.00 • To: Client A (Bank: ****1234)",
      reasoning:
        "Recurring monthly payment to known vendor. Flagged due to recent bank detail change.",
      expiresIn: "Expires in 4h",
    },
    {
      id: "approval-2",
      type: "email",
      title: "Email send request",
      detail: "To: new-client@unknown.com • Subject: Project Proposal - $5,000",
      reasoning: "New contact detected. Requires manual approval.",
      expiresIn: "Expires in 6h",
    },
  ],
  completedToday: 12,
  inProgress: 3,
  weeklyRevenue: [400, 650, 500, 350, 550, 0, 0],
  projectProgress: 75,
  tick: () =>
    set((state) => ({
      lastUpdated: "just now",
      status: state.status,
    })),
}));
