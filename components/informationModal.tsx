import useComponentVisible from "@/hooks/useComponentVisible";
import { InformationCircleIcon } from "@heroicons/react/24/outline";

export default function InformationModal({ text }: { text: string }) {
  const { ref, isComponentVisible, setIsComponentVisible } =
    useComponentVisible(false); // Handle closing when clicking outside

  return (
    <div className="relative inline-block text-left">
      <div ref={ref}>
        <button
          type="button"
          className="inline-flex justify-center w-6 text-gray-700"
          id="options-menu"
          aria-haspopup="true"
          aria-expanded="true"
          onClick={() => setIsComponentVisible(!isComponentVisible)}
        >
          <span className="sr-only">Open options</span>
          <InformationCircleIcon className="w-6" />
        </button>
      </div>
      <div
        className={
          "z-10 origin-top-right absolute right-0 w-56 rounded-md shadow-xl outline outline-1 outline-gray-300 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none transition-transform " +
          (isComponentVisible ? "scale-100" : "scale-0")
        }
        role="menu"
        aria-orientation="vertical"
        aria-labelledby="options-menu"
      >
        <div className="p-2.5 text-sm text-gray-500" role="none">
          {text}
        </div>
      </div>
    </div>
  );
}
