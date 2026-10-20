"""CLI wrapper around the same synthetic fixture generator packaged with the API."""
from services.api.app.stupay_core.corpus import GROUPS,ROOT,generate,make_case,write_corpus
if __name__=='__main__':
    import json
    print(json.dumps(write_corpus(),indent=2))
