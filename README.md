# kvpexpand
Python library to expand nested key-value-pairs with extended configuration to parse complex strings.

For example, the key-value pair:

  ```python
  {"key1" : "subkey1=one,subkey2=two"}
  ```

Becomes:
  ```python
  {
    "key1_subkey1" : "one",
    "key1_subkey2" : "two",
  }
  ```