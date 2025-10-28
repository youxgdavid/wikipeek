#!/usr/bin/env python3
"""
WikiPeek+ — Random Wikipedia summaries in your terminal ✨
Author: youxgdavid
"""

import wikipedia
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

console = Console()

def get_random_summary():
    title = wikipedia.random()
    summary = wikipedia.summary(title, sentences=2)
    return title, summary

def get_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return topic, summary
    except wikipedia.exceptions.DisambiguationError as e:
        return topic, f"[yellow]Too many results.[/] Try one of these: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return topic, "[red]No page found for that topic.[/]"

def main():
    parser = argparse.ArgumentParser(description="🧠 WikiPeek+: Fetch random or topic-based Wikipedia summaries.")
    parser.add_argument("-s", "--search", type=str, help="Search for a specific topic")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of random articles to fetch")
    parser.add_argument("--save", action="store_true", help="Save results to summaries.txt")

    args = parser.parse_args()
    results = []

    if args.search:
        title, summary = get_summary(args.search)
        results.append((title, summary))
    else:
        for _ in range(args.count):
            title, summary = get_random_summary()
            results.append((title, summary))

    for title, summary in results:
        console.print(
            Panel.fit(
                Text(f"{title}\n\n{summary}", justify="left"),
                title=f"📘 {title}",
                border_style="cyan"
            )
        )

    if args.save:
        with open("summaries.txt", "a", encoding="utf-8") as f:
            f.write(f"\n=== WikiPeek Session ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n")
            for title, summary in results:
                f.write(f"\n{title}\n{'-'*len(title)}\n{summary}\n")
        console.print("\n💾 [green]Summaries saved to summaries.txt![/]")

if __name__ == "__main__":
    main()

