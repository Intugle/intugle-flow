import { render } from "@testing-library/react";
import { LangflowCounts } from "../langflow-counts";

describe("LangflowCounts", () => {
  it("should_render_nothing_when_community_links_are_disabled", () => {
    const { container } = render(<LangflowCounts />);
    expect(container).toBeEmptyDOMElement();
  });
});
