export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 text-gray-800 px-4">
      <h1 className="text-4xl font-bold mb-4">Word Graph Explorer</h1>
      <p className="text-lg text-gray-600 max-w-xl text-center">
        Discover synonyms, antonyms, and collocations through an interactive word graph. Navigate to Search to begin exploring.
      </p>
      <a
        href="/search"
        className="mt-6 inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
      >
        Start Searching
      </a>
    </div>
  );
}
