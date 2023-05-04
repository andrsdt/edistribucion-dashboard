import { Card, Title } from "@tremor/react";
import Link from "next/link";

export default function UserWelcome() {
	return (
		<Card>
			<Title>¡Bienvenido!</Title>
			<p className="text-gray-500">
				Ten encuenta que tus datos de consumo pueden tardar hasta{" "}
				<b>72 horas</b> en llegar a los servidores. Ante cualquier duda,
				consulta tu consumo en la{" "}
				<Link href="https://zonaprivada.edistribucion.com/areaprivada/s/login">
					Zona privada de Edistribución
				</Link>
				.
			</p>
		</Card>
	);
}
