import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

// ==========================
// Manipal Hospitals Demo App
// ==========================
// Added: Link button that opens this app when clicked

const DOCTORS = [
  { id: 1, name: "Dr. Devi Shetty", dept: "Cardiac Surgery", location: "Old Airport Road" },
  { id: 2, name: "Dr. Manish Rai", dept: "Cardiology", location: "Old Airport Road" },
];

const TIME_SLOTS = ["09:00", "09:20", "09:40", "10:00", "10:20", "10:40", "11:00", "11:20", "11:40", "12:00"];

type Priority = "Normal" | "Urgent";

type Appointment = {
  time: string;
  patient: string;
  doctor: string;
  dept: string;
  emergency?: boolean;
  priority?: Priority;
};

const urgentFirstThenTime = (a: Appointment, b: Appointment) => {
  const ap = a.priority === "Urgent" ? 0 : 1;
  const bp = b.priority === "Urgent" ? 0 : 1;
  if (ap !== bp) return ap - bp;
  return a.time.localeCompare(b.time);
};

function parseToken(label: string): number | null {
  if (typeof label !== "string") return null;
  if (!label.startsWith("#")) return null;
  const n = parseInt(label.slice(1), 10);
  return Number.isNaN(n) ? null : n;
}

export default function HealthcareApp() {
  const [token, setToken] = useState<number | null>(23);
  const [ahead, setAhead] = useState(4);
  const avgConsultMins = 7;
  const estimatedWait = Math.max(0, ahead * avgConsultMins);

  const [currentToken, setCurrentToken] = useState(22);
  const [appointments, setAppointments] = useState<Appointment[]>([
    { time: "10:00", patient: "#21", doctor: "Dr. Manish Rai", dept: "Cardiology", priority: "Normal" },
    { time: "10:20", patient: "#22", doctor: "Dr. Manish Rai", dept: "Cardiology", priority: "Normal" },
    { time: "10:40", patient: "Emergency", doctor: "Triage", dept: "ER", emergency: true, priority: "Urgent" },
    { time: "11:00", patient: "#23", doctor: "Dr. Manish Rai", dept: "Cardiology", priority: "Normal" },
  ]);

  const waitingCount = appointments.length;

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
        <a
          href="https://your-demo-link.com"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block mt-2 text-blue-600 underline"
        >
          👉 Open Appointment App Demo
        </a>
      </div>

      <Card className="rounded-2xl shadow-lg border-blue-100">
        <CardContent className="p-6">
          <h2 className="text-xl font-bold mb-4 text-blue-700">📱 Patient App</h2>
          <div className="mt-6 space-y-4">
            <div className="p-4 bg-gradient-to-r from-blue-100 to-blue-50 rounded-xl border border-blue-200">
              <h3 className="font-semibold mb-1 text-blue-800">🎟️ Queue Tracker</h3>
              <p>Token Number: <b>#{typeof token === "number" ? token : "—"}</b></p>
              <p>Ahead of You: <b>{ahead} patients</b></p>
              <p>Estimated Wait: <b>{estimatedWait} mins</b></p>
              <Progress value={((5 - Math.min(5, ahead)) / 5) * 100} className="mt-2" />
            </div>

            {appointments.length > 0 && (
              <div className="p-4 bg-white rounded-xl border shadow">
                <h3 className="font-semibold mb-1">🗓️ Upcoming Appointment</h3>
                <p>
                  {appointments[0].doctor} ({appointments[0].dept}) {appointments[0].priority === "Urgent" && (
                    <span className="text-red-600 font-semibold">• Urgent</span>
                  )}
                </p>
                <p>
                  Date: <b>2025-08-20</b> • Slot: <b>{appointments[0].time}</b> • Token: <b>{appointments[0].patient}</b>
                </p>
                <div className="flex gap-2 mt-2">
                  <Button className="bg-green-600 hover:bg-green-700 text-white" onClick={handleNext}>
                    Next
                  </Button>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <Card className="rounded-2xl shadow-lg">
        <CardContent className="p-6">
          <h2 className="text-xl font-bold mb-2 text-green-700">💻 Doctor Dashboard</h2>
          <div className="mb-4 p-4 bg-green-50 rounded-xl">
            <h3 className="font-semibold">📋 Today's Appointments</h3>
            <ul className="list-disc list-inside">
              {appointments.map((a, idx) => (
                <li key={idx} className={a.priority === "Urgent" || a.emergency ? "font-bold text-red-600" : ""}>
                  {a.time} - Patient {a.patient} – {a.doctor} ({a.dept}) {a.priority === "Urgent" && (
                    <span className="ml-1 text-red-600">[Urgent]</span>
                  )}
                </li>
              ))}
            </ul>
          </div>

          <div className="mb-4 p-4 bg-yellow-50 rounded-xl">
            <h3 className="font-semibold">📊 Queue Overview</h3>
            <p>Current Token: <b>#{currentToken}</b></p>
            <p>Next: <b>#{currentToken + 1}</b></p>
            <p>Waiting Patients: <b>{waitingCount}</b></p>
            <div className="flex gap-2 mt-2">
              <Button onClick={handleNext}>➡️ Next Patient</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// ------------------ Basic Tests ------------------
console.assert(parseToken("#25") === 25, "parseToken should parse number");
console.assert(parseToken("A25") === null, "parseToken should reject invalid token");
console.assert(
  urgentFirstThenTime(
    { time: "09:00", patient: "#1", doctor: "D", dept: "X", priority: "Urgent" },
    { time: "08:00", patient: "#2", doctor: "D", dept: "X", priority: "Normal" }
  ) < 0,
  "Urgent should come before Normal"
);
console.assert(
  urgentFirstThenTime(
    { time: "09:00", patient: "#1", doctor: "D", dept: "X", priority: "Normal" },
    { time: "09:30", patient: "#2", doctor: "D", dept: "X", priority: "Normal" }
  ) < 0,
  "Earlier time should come first when priorities are equal"
);
console.assert(parseToken("#abc") === null, "parseToken should return null for non-numeric tokens");
