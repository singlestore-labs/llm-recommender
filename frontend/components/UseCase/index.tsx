import { UseCaseForm } from "./Form";

export function UseCase() {
  return (
    <div className="w-full max-w-3xl">
      <h2 className="text-2xl font-semibold leading-none tracking-tight">
        Describe your use case
      </h2>

      <UseCaseForm className="mb-32 mt-8" />
    </div>
  );
}
