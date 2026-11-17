import { useState } from "react";

// ==========================
// Manipal Hospitals Types
// ==========================

export type Priority = "Normal" | "Urgent";

export type Appointment = {
  time: string;
  patient: string;
  doctor: string;
  dept: string;
  emergency?: boolean;
  priority?: Priority;
  room?: string;
  status?: "Waiting" | "In Consultation" | "Completed" | "Deferred";
};

export const DOCTORS = [
  { id: 1, name: "Dr. Devi Shetty", dept: "Cardiac Surgery", room: "Room 101" },
  { id: 2, name: "Dr. Manish Rai", dept: "Cardiology", room: "Room 204" },
  { id: 3, name: "Dr. Sudarshan Ballal", dept: "Nephrology", room: "Room 305" },
  { id: 4, name: "Dr. Triage Team", dept: "ER / Emergency", room: "ER Bay 1" },
];

export const TIME_SLOTS = [
  "09:00", "09:20", "09:40", "10:00", "10:20",
  "10:40", "11:00", "11:20", "11:40", "12:00"
];

export const urgentFirstThenTime = (a: Appointment, b: Appointment): number => {
  const ap = a.priority === "Urgent" || a.emergency ? 0 : 1;
  const bp = b.priority === "Urgent" || b.emergency ? 0 : 1;
  if (ap !== bp) return ap - bp;
  return a.time.localeCompare(b.time);
};

export function parseToken(label: string): number | null {
  if (typeof label !== "string") return null;
  if (!label.startsWith("#")) return null;
  const n = parseInt(label.slice(1), 10);
  return Number.isNaN(n) ? null : n;
}

export default function HealthcareApp() {
  const [token] = useState<number | null>(23);
  const [ahead, setAhead] = useState(4);
  const avgConsultMins = 7;
  const estimatedWait = Math.max(0, ahead * avgConsultMins);

  const [currentToken, setCurrentToken] = useState(22);
  const [appointments, setAppointments] = useState<Appointment[]>([
    { time: "10:00", patient: "#21", doctor: "Dr. Manish Rai", dept: "Cardiology", priority: "Normal", room: "Room 204" },
    { time: "10:20", patient: "#22", doctor: "Dr. Manish Rai", dept: "Cardiology", priority: "Normal", room: "Room 204" },
    { time: "10:40", patient: "Emergency", doctor: "Triage", dept: "ER", emergency: true, priority: "Urgent", room: "ER Bay 1" },
    { time: "11:00", patient: "#23", doctor: "Dr. Manish Rai", dept: "Cardiology", priority: "Normal", room: "Room 204" },
  ]);

  const handleNext = () => {
    setAppointments((prev) => {
      if (prev.length === 0) return prev;
      const [served, ...rest] = prev;
      const parsed = parseToken(served.patient);
      if (parsed != null) setCurrentToken(parsed);
      else setCurrentToken((t) => t + 1);
      setAhead((a) => Math.max(0, a - 1));
      return rest;
    });
  };

  return (
    <div className="p-6 grid gap-6 md:grid-cols-2 bg-gradient-to-br from-blue-50 to-white min-h-screen">
      <div className="md:col-span-2 text-center mb-4">
        <h1 className="text-3xl font-extrabold text-blue-800">Manipal Hospitals Smart Queue System</h1>
        <p className="text-sm text-gray-600">
          Old Airport Road, Bengaluru • NABH Accredited • 700+ Beds • 60+ Specialties
        </p>
      </div>

      {/* Patient App */}
      <div className="rounded-2xl border bg-white shadow-lg p-6 border-blue-100">
        <h2 className="text-xl font-bold mb-4 text-blue-700">📱 Patient App</h2>
        <div className="p-4 bg-gradient-to-r from-blue-100 to-blue-50 rounded-xl border border-blue-200">
          <h3 className="font-semibold mb-1 text-blue-800">🎟️ Queue Tracker</h3>
          <p>Token Number: <b>#{token ?? "—"}</b></p>
          <p>Ahead of You: <b>{ahead} patients</b></p>
          <p>Estimated Wait: <b>{estimatedWait} mins</b></p>
        </div>
      </div>

      {/* Doctor Dashboard */}
      <div className="rounded-2xl border bg-white shadow-lg p-6">
        <h2 className="text-xl font-bold mb-2 text-green-700">💻 Doctor Dashboard</h2>
        <div className="p-4 bg-yellow-50 rounded-xl">
          <p>Current Token: <b>#{currentToken}</b></p>
          <p>Waiting Patients: <b>{appointments.length}</b></p>
          <button
            onClick={handleNext}
            className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            ➡️ Next Patient
          </button>
        </div>
      </div>
    </div>
  );
}
