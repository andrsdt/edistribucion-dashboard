import AccumulatedConsumption from "@/components/accumulatedConsumption";
import ConsumptionDifference from "@/components/consumptionDifference";
import ConsumptionGraph from "@/components/consumptionGraph";
import InstantPower from "@/components/instantPower";
import { Col, Grid } from "@tremor/react";
import PvpcPriceTracker from "../components/pvpcPriceTracker";

export default function Main() {
  const USES_PVPC = false;

  return (
    <main className="p-8 bg-gray-100 h-screen">
      <Grid numColsLg={6} className="gap-6 mt-6">
        {/* Main section */}
        <Col numColSpanLg={4}>
          <div className="space-y-6 h-full">
            <Grid numColsLg={2} className="gap-6">
              <ConsumptionDifference />
              <InstantPower />
            </Grid>
            <ConsumptionGraph />
          </div>
        </Col>

        {/* KPI sidebar */}
        <Col numColSpanLg={2}>
          <div className="space-y-6">
            <AccumulatedConsumption />
            <PvpcPriceTracker />
          </div>
        </Col>
      </Grid>
    </main>
  );
}
