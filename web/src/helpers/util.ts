import { MouseEvent } from "react";

export const dv = true; // dev mode
export const dbg = (...msg) => {
  dv && console.log(...msg);
  return msg;
};

export const tryCatch = async <T>(func: Promise<T>): Promise<T> => {
  try {
    return await func;
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error(`Error: ${error}`);
    return Promise.reject();
  }
};

export const wait = (ms) => new Promise((res) => setTimeout(res, ms));

const setDifference = <T>(A: Set<T>, B: Set<T>): Set<T> => {
  const diff = new Set(A);
  for (const item of B) {
    diff.delete(item);
  }
  return diff;
};

export const arrayDifference = <T>(A: T[], B: T[]): T[] => [
  ...setDifference(new Set(A), new Set(B)),
];

export const arrayUnique = <T>(A: T[]): T[] => [...new Set(A)];

// Implement git diff-esque between old cached & new remote songIds
// Used to selectively manipulate RxDB & only request new vectors, not all vectors (~20MB)
export const gitDiff = <T>(newArr: T[], oldArr: T[]): T[][] => {
  const newSet = new Set(newArr);
  const oldSet = new Set(oldArr);
  const addedChanges = [...setDifference(newSet, oldSet)];
  const deletedChanges = [...setDifference(oldSet, newSet)];
  return [addedChanges, deletedChanges];
};

// Concat all arrays of objects A,B by "key" key
export const concatById = <T, U>(a: T[], b: U[], key: string) => {
  const make = (arr): [Record<string, number>, Set<string>] => {
    const idIndexMap = Object.fromEntries(
      arr.map((obj, idx) => [obj[key], idx])
    );
    const idsSet = new Set(Object.keys(idIndexMap));
    return [idIndexMap, idsSet];
  };
  const [aMap, aSet] = make(a);
  const [bMap, bSet] = make(b);
  const unionIdsArr = [...new Set([...aSet, ...bSet])];
  const mergedArr = unionIdsArr.map((id) => ({
    ...(a[aMap[id]] ?? {}),
    ...(b[bMap[id]] ?? {}),
  }));
  return mergedArr;
};

export const filterInOut = <T>(arr: T[], key: string): [T[], T[]] => [
  arr.filter((el) => el[key]),
  arr.filter((el) => !el[key]),
];

export const test = () => {
  dbg(
    concatById(
      [{ a: "foo", b: "gah" }, { a: "eeh" }],
      [{ a: "foo", g: "wut" }],
      "a"
    )
  );
  dbg(
    filterInOut(
      concatById(
        [
          { id: 1, name: "Ben" },
          { id: 2, name: "Sally" },
        ],
        [{ id: 1, vector: [1, 2] }],
        "id"
      ),
      "vector"
    )
  );
};

export const openInApp = (uri) => {
  const domainEnds = uri.indexOf("/", "https://".length) + 1;
  const uriPart = uri.slice(domainEnds).replace(/\//g, ":");

  return `spotify:${uriPart}`;
};

// Linear backoff.
export const retryAsync = <T extends Array<any>, U>(
  fn: (...args: T) => Promise<U>
) => {
  return async function (...args: T): Promise<U> {
    for (let depth = 0; depth < 50; depth++) {
      try {
        return await fn(...args);
      } catch (e) {
        await wait(500);
      }
    }
    return Promise.reject();
  };
};

export type ButtonCallback = (e: MouseEvent<HTMLButtonElement>) => any;
export type DivCallback = (e: MouseEvent<HTMLDivElement>) => any;
