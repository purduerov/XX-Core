# Pakfront
Proxy that routes traffic between the frontend and ROV. Logs shit, passes image data to CV

##Pakfront and Running it: What does it do? How do you install it? Let's find out
pakfront is written in Go, which is a compiled language, like C, but they build system is way less convoluted. For our purposes, the final product we are looking for is a binary named "panzerkanone" which can be run like any other executable(it also needs a config file, but that just sits in surface), and some python scripts that can be run as CV subprocesses. This all sits in the pakfront/bin/ directory, which one can run at his or her own leisure.

### Installation


