import certstream
import yaml

from tld import get_tld

'''
Use CaliDog certstream URL for testing purposes.
It is recommended that you run your own CertStream Server
for better results/higher data throughput
'''
certstream_url = 'wss://certstream.calidog.io'
# certstream_url = 'ws://127.0.0.1:4000'
domain_log = 'phishing_domains.txt'


'''
Filter out top 1M domains to reduce false positives
Source: Umbrella 1M (http://s3-us-west-1.amazonaws.com/umbrella-static/index.html)
'''
whitelist = set()
with open('top-1m.csv','r') as f:
    for line in f:
        whitelist.add(line.strip().split(',')[1])

longlist = set()

def score_domain(domain):
    # Remove certificate wildcard from CTL data
    if domain.startswith('*.'):
        domain = domain[2:]

    # Append http:// to domain for tld library to work
    domain = 'http://' + domain

    '''
    Split into constituent parts to filter out well known domains
    and scoring component
    '''
    try:
        result = get_tld(domain, as_object=True, fix_protocol=True, fail_silently=True)
        domain = '.'.join([result.subdomain, result.domain])
        check_domain = '.'.join([result.domain, result.tld])
        check_tld = result.tld
    except:
        check_domain = domain
        check_tld = ''

    # Filter out domains that match the Umbrella 1M (reduce false positives)
    if check_domain in whitelist:
        return 0

    score = 0
    # Additional score based on tld (worst offenders from Spamhaus rankings)
    if check_tld in scoring['twotlds']:
        score += 2
    elif check_tld not in scoring['zerotlds']:
        score += 1

    # Check keyword matches
    for word in scoring['keywords']:
        if word in domain:
            score += scoring['keywords'][word]

    # Check brand matches
    for word in scoring['brands']:
        if word in domain:
            score += scoring['brands'][word]

    return score


def callback(message, context):
    # Callback handler for certstream events (boilerplate from CaliDog Github)
    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        for domain in all_domains:
            # Filter domain if we have already seen it (prevent duplication)
            if domain in longlist:
                continue
            longlist.add(domain)
            score = score_domain(domain.lower())

            # If score exceeds threshold, write data to phishing log
            if score >= 7:
                with open(domain_log, 'a') as f:
                    f.write("{}\n".format(domain))


if __name__ == '__main__':
    with open('scoring.yml', 'r') as f:
        scoring = yaml.safe_load(f)

    certstream.listen_for_events(callback, url=certstream_url)
