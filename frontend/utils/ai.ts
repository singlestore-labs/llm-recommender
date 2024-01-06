import * as tiktoken from "js-tiktoken";

const tokensEncoding = tiktoken.getEncoding("cl100k_base");

export function countTokens(text: string) {
  return tokensEncoding.encode(text).length;
}

export function splitText(text: string, maxTokens = 2040) {
  if (countTokens(text) <= maxTokens) return text;

  const separator = " ";
  const words = text.split(separator);
  const chunks: string[] = [];
  let currentChunkWords: string[] = [];

  for (const word of words) {
    const tokens = countTokens([...currentChunkWords, word].join(separator));

    if (tokens <= maxTokens) {
      currentChunkWords.push(word);
    } else {
      chunks.push(currentChunkWords.join(separator));
      currentChunkWords = [word];
    }
  }

  if (currentChunkWords.length) {
    chunks.push(currentChunkWords.join(separator));
  }

  return chunks;
}
