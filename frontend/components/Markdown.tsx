import ReactMarkdown from "react-markdown";
import RemarkGfm from "remark-gfm";
import RehypeHighlight from "rehype-highlight";
import RehypeRaw from "rehype-raw";
import Link from "next/link";
import "./Markdown.css";

import { ComponentProps } from "@/types";
import { cn } from "@/utils";

export type MarkdownProps = ComponentProps<{
  children?: string;
  className?: string;
}>;

export function Markdown({ children, className }: MarkdownProps) {
  return (
    <ReactMarkdown
      rehypePlugins={[RehypeHighlight, RehypeRaw]}
      remarkPlugins={[[RemarkGfm]]}
      className={cn("markdown-body", className)}
      components={{
        a: ({ href, children }) => {
          if (!href) return <>{children}</>;
          const isExternal = /^http/.test(href);
          return (
            <Link href={href} target={isExternal ? "_blank" : undefined}>
              {children}
            </Link>
          );
        },
      }}
    >
      {children}
    </ReactMarkdown>
  );
}
