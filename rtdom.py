import tldextract

input_file_path = input("Please enter the path to your input file: ")

with open(input_file_path, 'r') as file:
    input_urls = file.read().splitlines()

filtered_domains = set()
for url in input_urls:
    extracted = tldextract.extract(url)
    if extracted.domain and extracted.suffix:
        full_domain = f"{extracted.domain}.{extracted.suffix}"
        filtered_domains.add(full_domain)

sorted_filtered_domains = sorted(filtered_domains)

print("Filtered and sorted domains:", sorted_filtered_domains)

output_file_path = input("Please enter the name of the output file (e.g., output.txt): ")

with open(output_file_path, 'w') as output_file:
    for domain in sorted_filtered_domains:
        output_file.write(domain + '\n')

print(f"The filtered domains have been saved to {output_file_path}.")