"""CLI wrapper around isolated, deterministic API-shared core policy evaluator."""
from services.api.app.stupay_core.evaluator import POLICIES,checks,decide,metrics,run
if __name__=='__main__':
    import argparse,json
    p=argparse.ArgumentParser();p.add_argument('--split',choices=['holdout','development','all'],default='holdout');p.add_argument('--out',default='benchmarks/results');a=p.parse_args()
    print(json.dumps(run(a.split,a.out),indent=2))
