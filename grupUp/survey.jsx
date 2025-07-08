import react, { useState } from "react";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";

const schema = require("./schema.json"); // Assuming you saved the JSON schema separately

export default function SurveyFrontend() {
  const [answers, setAnswers] = useState({});
  const [currentStep, setCurrentStep] = useState(0);

  const keys = Object.keys(schema);
  const totalRequired = keys.filter(
    (key) => !schema[key].optional
  ).length;

  const handleChange = (questionKey, value) => {
    setAnswers((prev) => ({ ...prev, [questionKey]: value }));
  };

  const currentKey = keys[currentStep];
  const current = schema[currentKey];

  const handleNext = () => {
    if (currentStep < keys.length - 1) setCurrentStep(currentStep + 1);
  };

  const handleBack = () => {
    if (currentStep > 0) setCurrentStep(currentStep - 1);
  };

  const isAnswered = (key) => answers[key] !== undefined;

  const percentDone =
    (Object.keys(answers).filter((k) => isAnswered(k)).length /
      totalRequired) *
    100;

  return (
    <div className="max-w-xl mx-auto p-4">
      <Progress value={percentDone} className="mb-4" />

      <div className="text-lg font-semibold mb-2">{current.question}</div>

      {/* Render basic types */}
      {current.type === "multi-select" && (
        <div className="flex flex-wrap gap-2">
          {current.options.map((opt) => (
            <button
              key={opt}
              onClick={() => {
                const prev = answers[currentKey] || [];
                handleChange(
                  currentKey,
                  prev.includes(opt)
                    ? prev.filter((o) => o !== opt)
                    : [...prev, opt]
                );
              }}
              className={`px-4 py-2 rounded-full border text-sm ${
                answers[currentKey]?.includes(opt)
                  ? "bg-blue-500 text-white"
                  : "bg-white text-black"
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      )}

      {current.type === "scale" && (
        <div className="flex flex-col gap-2">
          <input
            type="range"
            min={current.min}
            max={current.max}
            step={current.step}
            value={answers[currentKey] || current.min}
            onChange={(e) => handleChange(currentKey, Number(e.target.value))}
          />
          <div className="flex justify-between text-xs">
            {Object.entries(current.labels).map(([pos, label]) => (
              <span key={pos} className="w-1/3 text-center">
                {label}
              </span>
            ))}
          </div>
        </div>
      )}

      {current.type === "select" && (
        <div className="flex flex-col gap-2">
          {current.options.map((opt) => (
            <label key={opt} className="inline-flex items-center gap-2">
              <input
                type="radio"
                name={currentKey}
                value={opt}
                checked={answers[currentKey] === opt}
                onChange={() => handleChange(currentKey, opt)}
              />
              {opt}
            </label>
          ))}
        </div>
      )}

      {current.type === "text" && (
        <textarea
          rows={current.multiline ? 3 : 1}
          className="w-full border p-2 mt-2"
          placeholder="Type your answer..."
          value={answers[currentKey] || ""}
          onChange={(e) => handleChange(currentKey, e.target.value)}
        />
      )}

      <div className="flex justify-between mt-6">
        <Button onClick={handleBack} disabled={currentStep === 0}>
          Back
        </Button>
        <Button onClick={handleNext}>
          {currentStep === keys.length - 1 ? "Finish" : "Next"}
        </Button>
      </div>
    </div>
  );
}
