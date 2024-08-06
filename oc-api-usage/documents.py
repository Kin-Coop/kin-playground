
GET_HOST = '''
query (
  $slug: String
) {
  host(
    slug: $slug
  ) {
    id
    slug
    type
    name
    legalName
  }
}
'''
