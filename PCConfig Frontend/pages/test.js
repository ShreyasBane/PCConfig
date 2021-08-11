import Search from "../components/SearchCard";
import Filter from "../components/Filter";

export default function Test({ data }) {
  const testcase = [
    {
      name: "Manufacturer",
      options: ["AMD", "Intel"]
    },
    {
      name: "Microarchitecture",
      options: ["Zen"]
    },
    {
      name: "Core Count",
      options: [4]
    },
    {
      name: "No of Threads",
      options: [4]
    },
    {
      name: "Socket",
      options: ["AM4"]
    }
  ];
  return (
    <>
      <Filter items={testcase} onChange={(e) => console.log(e)} />
    </>
  );
}

export async function getStaticProps() {
  const res = await fetch("https://pcconfig.shreyasbane.repl.co/search");
  const data = await res.json();
  return {
    props: {
      data
    }
  };
}
