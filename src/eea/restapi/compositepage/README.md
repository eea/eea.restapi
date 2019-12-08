We introduce and enforce the concept of "Composite Page".

The Composite Page is a universal container.

- it is always a folder internally, but it can have a cameleon-like behaviour:
  switch its layout to a listing view, it behaves like a folder, switch to
  composite view, then it behaves like a Composite page (Volto blocks-based
  Page). Folders are just aliases of this universal type, with the
  default view set to listing view.

Volto (somewhat) allows switching the View to use blocks-based layout, but that
is not possible for the Edit form. Volto detects blocks layout based on the
presence of properties with names that end with "blocks" and decides the Edit
form implementation based on this. To override this mechanism, we override the
serialization of DX Content and remove these properties if the context doesn't
have the composite layout view.

