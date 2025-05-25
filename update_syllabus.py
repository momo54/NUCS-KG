import argparse
from rdflib import Graph

def run_update(input_file, output_file):
    g = Graph()
    g.parse(input_file, format="turtle")

    sparql_update = """
    PREFIX course: <http://example.org/course/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

DELETE {
  ?s course:responsible ?anyResponsible .
}
INSERT {
  ?s course:syllabus ?UE .
}
WHERE {
  {
    SELECT ?s ?UE WHERE {
      {
        SELECT ?s
               (GROUP_CONCAT(DISTINCT ?label; separator=", ") AS ?labels)
               (GROUP_CONCAT(DISTINCT ?content; separator="\\n- ") AS ?contents)
               (GROUP_CONCAT(DISTINCT ?objective; separator="\\n- ") AS ?objectives)
        WHERE {
          ?s rdfs:label ?label .
          ?s course:content ?content .
          ?s course:objective ?objective .
        }
        GROUP BY ?s
      }
      BIND(CONCAT(
        "\\n Course Name: ", STR(?labels),
        "\\n Objectives: ", STR(?objectives),
        "\\n Course content: ", STR(?contents)
      ) AS ?UE)
    }
  }
  OPTIONAL { ?s course:responsible ?anyResponsible }
}   """

    g.update(sparql_update)
    g.serialize(destination=output_file, format="turtle")
    print(f"✅ Updated graph written to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply SPARQL DELETE/INSERT to RDF file.")
    parser.add_argument("input", help="Input TTL file")
    parser.add_argument("output", help="Output TTL file")
    args = parser.parse_args()

    run_update(args.input, args.output)
