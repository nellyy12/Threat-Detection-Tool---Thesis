import argparse
import os
import json

from scrapers.pastebin_scraper import scrape_pastebin, scrape_pastebin_psbdmp
from scrapers.reddit_scraper import scrape_reddit
from scrapers.github_scraper import scrape_github
from scrapers.twitter_scraper import scrape_twitter
from scrapers.hackedlist_scraper import hackedlist

PLATFORMS = ["pastebin", "reddit", "github", "twitter", "hackedlist"]

SCRAPER_FUNCS = {
    "reddit": scrape_reddit,
    "github": scrape_github,
    "twitter": scrape_twitter,
    "hackedlist": hackedlist,
}

def main():
    parser = argparse.ArgumentParser(
        description="Scrape data from various platforms for a given organization/domain."
    )
    parser.add_argument(
        "-d", "--domain", required=True, help="Target organization or domain (e.g., example.com)"
    )
    parser.add_argument(
        "--platforms", nargs="*", choices=PLATFORMS, help="Platforms to scrape (default: all if --all is set)"
    )
    parser.add_argument(
        "--all", action="store_true", help="Scrape all supported platforms. Overrides --platforms."
    )
    parser.add_argument(
        "--output-dir", default="output", help="Directory to save output files."
    )
    args = parser.parse_args()

    if args.all or not args.platforms:
        platforms = PLATFORMS
    else:
        platforms = args.platforms

    os.makedirs(args.output_dir, exist_ok=True)

    for platform in platforms:
        print(f"[+] Scraping {platform.title()} for {args.domain}")
        if platform == "pastebin":
            # Run both Google scraping and psbdmp API for all three search types
            data_google = scrape_pastebin(args.domain)
            out_path_google = os.path.join(
                args.output_dir, f"{args.domain.replace('.', '_')}_pastebin_google.txt"
            )
            with open(out_path_google, "w", encoding="utf-8") as f:
                f.write(json.dumps(data_google, indent=2, ensure_ascii=False))
            print(f"    Saved Google scraping results to {out_path_google}")

            for search_type in ["general", "email", "domain"]:
                data_psbdmp = scrape_pastebin_psbdmp(args.domain, search_type)
                out_path_psbdmp = os.path.join(
                    args.output_dir, f"{args.domain.replace('.', '_')}_pastebin_psbdmp_{search_type}.txt"
                )
                with open(out_path_psbdmp, "w", encoding="utf-8") as f:
                    f.write(json.dumps(data_psbdmp, indent=2, ensure_ascii=False))
                print(f"    Saved psbdmp.ws {search_type} results to {out_path_psbdmp}")
        else:
            scraper = SCRAPER_FUNCS.get(platform)
            if scraper:
                try:
                    data = scraper(args.domain)
                except Exception as e:
                    data = {"error": str(e)}
            else:
                data = {"error": "Scraper not implemented."}
            out_path = os.path.join(
                args.output_dir, f"{args.domain.replace('.', '_')}_{platform}.txt"
            )
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"    Saved results to {out_path}")

if __name__ == "__main__":
    main() 