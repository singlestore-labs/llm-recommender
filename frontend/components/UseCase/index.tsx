import { Heading } from "@/components/Heading";
import { UseCaseForm } from "./Form";

export function UseCase() {
  return (
    <div className="w-full max-w-3xl">
      <Heading as="h2">Describe your use case</Heading>
      <UseCaseForm className="mb-32 mt-8" />
    </div>
  );
}
