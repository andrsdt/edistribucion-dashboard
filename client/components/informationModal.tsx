import useComponentVisible from "@/hooks/useComponentVisible";
import { InformationCircleIcon } from "@heroicons/react/24/outline";

const ORIGINS = {
	"top-right": "origin-top-right",
	"top-left": "origin-top-left",
	"bottom-right": "origin-bottom-right",
	"bottom-left": "origin-bottom-left",
};

const POSITIONS = {
	"top-right": "right-0",
	"top-left": "left-0",
	"bottom-right": "right-0",
	"bottom-left": "left-0",
};

export default function InformationModal({
	text,
	origin = "top-right",
}: {
	text: string;
	origin: keyof typeof ORIGINS;
}) {
	const { ref, isComponentVisible, setIsComponentVisible } =
		useComponentVisible(false); // Handle closing when clicking outside

	return (
		<div className="relative inline-block text-left translate-y-0.5 z-50">
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
					"z-10 absolute w-56 rounded-md shadow-xl outline outline-1 outline-gray-300 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none transition-transform " +
					POSITIONS[origin] +
					" " +
					ORIGINS[origin] +
					" " +
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
