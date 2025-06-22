import time
import library
from prime_generator import set_primes

def check_lib(lib, unique_words, word_to_books, book_titles, sort_output=True):
    all_passed = True

    # Distinct words & count check
    for i, book in enumerate(book_titles):
        dw = lib.distinct_words(book)
        if dw is None or (sort_output and sorted(dw) != sorted(unique_words[i])) or (not sort_output and dw != unique_words[i]):
            print(f"DISTINCT WORDS FAILED! ({book})")
            all_passed = False
        if lib.count_distinct_words(book) != len(unique_words[i]):
            print(f"COUNT DISTINCT WORDS FAILED! ({book})")
            all_passed = False

    # Keyword search check
    for word in set(w for words in unique_words for w in words):
        expected_books = sorted(word_to_books[word])
        result_books = lib.search_keyword(word)
        if sort_output:
            result_books.sort()
        if result_books != expected_books:
            print(f"SEARCH KEYWORD FAILED! (\"{word}\")")
            all_passed = False

    if all_passed:
        print("✅ ALL TESTS PASSED!\n")
    else:
        print("❌ SOME TESTS FAILED!\n")




def get_primes(start=10 * 3, end=10 * 5):
    is_prime = [True] * (end + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, end + 1):
        if not is_prime[i]: continue

        for j in range(2 * i, end + 1, i):
            is_prime[j] = False

    prime_sizes = []
    sz = start
    while sz <= end:
        if not is_prime[sz]:
            sz += 1
            continue

        prime_sizes.append(sz)
        sz *= 2

    prime_sizes.reverse()
    return prime_sizes


def main():
    book_titles = ["bookone", "booktwo"]
    texts = [["The", "name", "of", "this", "book", "contains", "a", "number"],
             ["You", "can", "name", "this", "book", "anything"]]
    text1 = [text for text in texts]
    unique_words = []

    for text in texts:
        unique = []
        for word in text:
            if word not in unique:
                unique.append(word)
        unique_words.append(sorted(unique))

    word_to_books = {}
    for book, texts in zip(book_titles, texts):
        for word in texts:
            if word not in word_to_books:
                word_to_books[word] = [book]
            else:
                word_to_books[word].append(book)

    set_primes(get_primes())

    # Check Musk
    musk_time = time.perf_counter()
    musk_lib = library.MuskLibrary(book_titles, text1)
    musk_time = time.perf_counter() - musk_time

    print(f"Musk Library sorting took {musk_time}s")
    print(f"Checking Library functions for Musk:")
    check_lib(musk_lib, unique_words, word_to_books, book_titles)

    jobs_lib = library.JGBLibrary("Jobs", (10, 29))
    gates_lib = library.JGBLibrary("Gates", (10, 37))
    bezos_lib = library.JGBLibrary("Bezos", (10, 37, 7, 13))

    for lib, name in zip([jobs_lib, gates_lib, bezos_lib], ["Jobs", "Gates", "Bezos"]):
        time_taken = time.time()
        for book, text in zip(book_titles, text1):
            lib.add_book(book, text)
        time_taken = time.time() - time_taken
        print(f"{name} Library took {time_taken:.4f}s")
        print(f"Checking Library Functions for {name}: ")
        check_lib(lib, unique_words, word_to_books, book_titles)


def more_tests():
    print("======== CUSTOM TEST CASES =========")

    book_titles = ["alpha", "beta", "gamma", "delta"]
    texts = [
        ["a", "b", "c", "d", "e", "f", "g"],
        ["z", "y", "x", "w", "v", "u", "t", "s"],
        ["hello", "world", "hash", "table", "dynamic", "rehash", "check"],
        ["apple", "banana", "apple", "banana", "cherry", "durian"]
    ]

    word_to_books = {}
    unique_words = []

    for book, words in zip(book_titles, texts):
        uniq = []
        for word in words:
            if word not in uniq:
                uniq.append(word)
            if word not in word_to_books:
                word_to_books[word] = [book]
            else:
                if book not in word_to_books[word]:
                    word_to_books[word].append(book)
        unique_words.append(sorted(uniq))

    musk_lib = library.MuskLibrary(book_titles, texts)
    print("MuskLibrary:")
    check_lib(musk_lib, unique_words, word_to_books, book_titles)

    for name, params in [
        ("Jobs", (10, 13)),
        ("Gates", (10, 13)),
        ("Bezos", (10, 13, 7, 11))
    ]:
        lib = library.JGBLibrary(name, params)
        for title, text in zip(book_titles, texts):
            lib.add_book(title, text)
        print(f"{name}Library:")
        check_lib(lib, unique_words, word_to_books, book_titles)


if __name__ == "__main__":
    main()
    more_tests()
