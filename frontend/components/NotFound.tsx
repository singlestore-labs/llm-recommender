import { ReactNode } from "react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Heading } from "./Heading";

export default function CustomNotFound({ title }: { title: ReactNode }) {
  return (
    <div className="mb-32 flex flex-1 flex-col items-center justify-center">
      <Heading as="h2" className="flex flex-col text-4xl">
        <span className="text-[4em] leading-tight">404</span>
        <span>{title}</span>
      </Heading>
      <Button asChild className="mt-16">
        <Link href="/">Return Home</Link>
      </Button>
    </div>
  );
}
